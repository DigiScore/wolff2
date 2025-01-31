import logging
from random import random, randrange
from threading import Thread
from time import sleep, time

import config
from nebula.hivemind import DataBorg


class Conducter:
    """
    Controls movement and shapes drawn by the robot.
    """
    def __init__(self, speed: int = 5):

        self.XARM_CONNECTED = config.xarm_connected

        if self.XARM_CONNECTED:
            from modules.draw_xarm import Drawbot

            port = config.xarm1_port
            self.drawbot = Drawbot(port)

        else:
            self.drawbot = None

        # Own the dataclass
        self.hivemind = DataBorg()

        # Start operating vars
        self.current_phrase_num = 0  # number of phrases looped through, can be used to change behaviour over time...
        self.joint_inc = 10          # scaling factor for incremental movement
        self.continuous_mode = 0     # mode for continuous module. 0 == on page, 1 == above page
        self.continuous_source = 0   # source of data used for continous movement. 0 == random, 1 == NN, 2 == peak
        self.global_speed = speed
        self.mic_in_prediction = config.mic_in_prediction

        # Get the baseline temperature from config
        self.temperature = config.temperature

        # inherit scripted test object
        # self.scripted_experiment = ScriptedExperiment()


        # # if self.drawbot:
        # #     self.drawbot.home()
        #     # self.drawbot.go_position_draw()
        #
        # input('To start press ENTER when robot stops')
        #     # print('Going to draw position...')
        #     # input('Adjust pen height, then press ENTER')
        #     # self.drawbot.go_position_one_two()
        #     self.drawbot.go_position_ready()

    def main_loop(self, experiment_mode):
        """
        Starts the main thread for the gesture manager
        """
        if self.drawbot:
            self.drawbot.go_position_draw()
        # self.drawbot.go_position_draw()

        # input('To start press ENTER when robot stops')

        gesture_thread = Thread(target=self.gesture_manager, args=[experiment_mode,])
        gesture_thread.start()

        if self.drawbot:
            position_thread = Thread(target=self.drawbot.get_normalised_position)
            position_thread.start()
            # position_thread.join()
            self.drawbot.command_list_main_loop()

    def gesture_manager(self, experiment_mode=0):
        """
        Listens to the realtime incoming signal and calculates an affectual
        response based on general boundaries:
            HIGH   - if input stream is LOUD (0.8+) then emit, smash a random
                     fill and break out to Daddy cycle.
            MEDIUM - if input energy is 0.1-0.8 then emit, a jump out of child
                     loop.
            LOW    - nothing happens, continues with cycles.
        """

        if self.drawbot:
            # if experiment_mode != 3:

            print("Started robot control thread")
            # self.drawbot.home()
        else:
            print("Started robot control thread - no robot")

        # Names for affect listening
        stream_list = config.stream_list
        stream_list_len = len(stream_list)

        # self.temp_gesture_capture_list = []
        self.elapsed_time = time()

        while self.hivemind.running:
            ###################################################################
            # Phrase-level gesture gate: 3 - 8 seconds
            ###################################################################
            if self.XARM_CONNECTED:
                if experiment_mode != 3:
                    self.drawbot.random_pen()

            # Flag for breaking a phrase from big affect signal
            self.hivemind.interrupted = False

            # Clear command list at start of each gesture cycle
            if self.drawbot:
                if experiment_mode != 3:
                    self.drawbot.clear_commands()

            # Get length of gesture
            phrase_length = (randrange(300, 800) / 100)  # + self.global_speed
            phrase_loop_end = time() + phrase_length

            logging.info(f"======== GESTURE - Daddy cycle started ========")
            logging.info(f"Duration =  {phrase_length} seconds")

            ###################################################################
            # Randomly pick an input stream for this cycle
            # (either mic_in or stream in config.stream_list)
            ###################################################################

            if experiment_mode == 0:
                """
                A Normal Mode
                """
                if random() < self.mic_in_prediction:
                    rnd_stream = 'mic_in'
                else:
                    rnd = randrange(stream_list_len)
                    rnd_stream = stream_list[rnd]

            elif experiment_mode == 1:
                """
                B Random poetry
                """
                rnd_stream = 'rnd_poetry'

            elif experiment_mode == 2:
                """
                C Human only input
                """
                rnd_stream = 'mic_in'

            elif experiment_mode == 3:
                """
                D Pre defined scripted moves only
                """
                # start eroor checker
                self.doing_script = True
                script_thread = Thread(target=self.scripted_move_clear_alarms)
                script_thread.start()

                # run through fixed experiment scrip[t
                self.scripted_move()
                self.hivemind.running = False
                self.hivemind.MASTER_RUNNING = False
                break

            self.hivemind.thought_train_stream = rnd_stream
            logging.info(f"Random stream = {self.hivemind.thought_train_stream}")

            while time() < phrase_loop_end:
                ###############################################################
                # Rhythm-level gesture gate: .5-2 seconds
                ###############################################################

                # if a major break out then go to Daddy cycle and restart
                if self.hivemind.interrupted:
                    logging.info("----------------STREAM INTERRUPT----------------")
                    break

                # Clear the alarms
                if self.drawbot:
                    self.drawbot.clear_alarms()

                # Generate rhythm rate here
                rhythm_loop_end_time = time() + (randrange(500, 2000) / 1000)
                logging.debug(f'end time = {rhythm_loop_end_time}')

                # Speed for this phrase
                arm_speed = randrange(30, 200)
                if self.XARM_CONNECTED:
                    self.drawbot.set_speed(arm_speed)

                while time() < rhythm_loop_end_time:
                    ###########################################################
                    # Stream the chosen data around a loop
                    ###########################################################

                    # Make master output the current value of affect stream
                    # 1. Go get the current value from dict
                    thought_train = getattr(self.hivemind, rnd_stream)
                    logging.debug(f'======== RHYTHM cycle ========'
                                  f'|Affect stream output {rnd_stream}'
                                  f' == {thought_train}')

                    # 2. Send to Master Output
                    self.hivemind.master_stream = thought_train

                    ###########################################################
                    # Makes a response to chosen thought stream
                    ###########################################################
                    # [HIGH response]
                    if thought_train > 0.8 or self.hivemind.interrupted:
                        logging.info('Interrupt > !!! HIGH !!!')

                        # A - Refill dict with random
                        self.hivemind.randomiser()

                        # B - Jumps out of this loop into daddy
                        # (will clear commands by detecting interupt_clear)
                        self.hivemind.interrupted = True

                        # C - Respond
                        if self.drawbot:
                            self.high_energy_response()

                        # D- Break out of this loop, and next because of flag
                        sleep(0.1)
                        break

                    # [LOW response]
                    elif thought_train < 0.1:
                        logging.info('Interrupt < LOW : no response')
                        if self.drawbot:
                            if random() < 0.36:
                                self.design_move(thought_train)

                    # [MEDIUM response]
                    else:
                        if self.drawbot:
                            self.design_move(thought_train)

                    sleep(0.1)

        if self.drawbot:
                self.drawbot.go_position_ready()
        logging.info('quitting director thread')
        self.hivemind.MASTER_RUNNING = False

        # print gesture list for "scripted list test"
        # print("======================= temp_gesture_capture_list", self.temp_gesture_capture_list)
        # self.terminate()

    def design_move(self, thought_train):
        """
        Takes a thought train value and maps it to one of 10 functions, salvaged from Jess+ belief module.
        Due to the high energy interrupt in gesture manager this range is: 0.0 - 0.8
        """

        # get current position
        x, y = self.drawbot.get_pose()[:2]
        arc_range = thought_train * 10

        # make a random choice (for now)
        # todo - maybe map these across the range of input thought-trains
        randchoice = randrange(12)
        logging.debug(f'Random choice: {randchoice}')

        match randchoice:
            case 0:
                decision_type = 'draw line'
                paramx = x + self.rnd(thought_train*10)
                paramy = x + self.rnd(thought_train*10)
                self.drawbot.go_draw(paramx,
                                     paramy,
                                     False)
                # self.temp_gesture_capture_list.append([time() - self.elapsed_time, "self.drawbot.go_draw(x, y, False)", paramx, paramy, False])

            case 1:
                decision_type = 'random character'
                param = thought_train * randrange(10, 20)
                self.drawbot.draw_random_char(param)
                # self.temp_gesture_capture_list.append([time() - self.elapsed_time, "self.drawbot.draw_random_char(param)", param])

            case 2:
                decision_type = 'dot'
                self.drawbot.dot()
                # self.temp_gesture_capture_list.append([time() - self.elapsed_time, "self.drawbot.dot"])

            case 3:
                decision_type = 'note head'
                note_size = randrange(1, 10)
                self.drawbot.note_head(size=note_size)
                # self.temp_gesture_capture_list.append([time() - self.elapsed_time, "self.drawbot.note_head(note_size)", note_size])

            case 4:
                decision_type = 'note head and line'
                note_size = randrange(1, 10)
                self.drawbot.note_head(size=note_size)
                # self.temp_gesture_capture_list.append([time() - self.elapsed_time, "self.drawbot.note_head(note_size)", note_size])

                paramx = self.rnd(thought_train*10)
                paramy = self.rnd(thought_train*10)
                self.drawbot.position_move_by(paramx,
                                              paramy,
                                              0, wait=True)
                # self.temp_gesture_capture_list.append([time() - self.elapsed_time, "self.drawbot.position_move_by(paramx, paramy,0, wait=True)", paramx, paramy])

            case 5:
                decision_type = 'random jump'
                self.drawbot.go_random_jump()
                # self.temp_gesture_capture_list.append([time() - self.elapsed_time, "self.drawbot.go_random_jump()"])

            case 6:
                decision_type = 'draw arc'
                x1 = x + self.rnd(arc_range)
                y1 = y + self.rnd(arc_range)
                x2 = x + self.rnd(arc_range)
                y2 = y + self.rnd(arc_range)
                self.drawbot.arc2D(x1, y1, x2, y2)
                # self.temp_gesture_capture_list.append([time() - self.elapsed_time, "self.drawbot.arc2D(x1, y1, x2, y2)", x1, y1, x2, y2])

            case 7:
                decision_type = 'small squiggle'
                squiggle_list = []
                for _ in range(randrange(3, 9)):
                    squiggle_list.append((self.rnd(arc_range),
                                          self.rnd(arc_range),
                                          self.rnd(arc_range)))
                self.drawbot.squiggle(squiggle_list)
                # self.temp_gesture_capture_list.append([time() - self.elapsed_time, "self.drawbot.squiggle(squiggle_list)", squiggle_list])

            case 8:
                decision_type = 'draw circle'
                side = randrange(2)
                x1 = int(arc_range)
                self.drawbot.draw_circle(x1, side)
                # self.temp_gesture_capture_list.append([time() - self.elapsed_time, "self.drawbot.draw_circle(x1, side)", x1, side])

            case 9:
                decision_type = 'arc'
                x1 = x + self.rnd(arc_range)
                y1 = y + self.rnd(arc_range)
                self.drawbot.go_draw(x1, y1)
                # self.temp_gesture_capture_list.append([time() - self.elapsed_time, "self.drawbot.go_draw(x1, y1)", x1, y1])

            case 10:
                decision_type = 'return to coord'
                self.drawbot.return_to_coord()
                # self.temp_gesture_capture_list.append([time() - self.elapsed_time, "self.drawbot.return_to_coord()"])

            # case 11:
            #     decision_type = 'random shape group'
            #     self.drawbot.create_shape_group()
            #     # self.drawbot.repeat_shape_group()

            case 11:
                decision_type = 'random pen move'
                self.drawbot.random_pen()
                # self.temp_gesture_capture_list.append([time() - self.elapsed_time, "self.drawbot.random_pen()"])

        # make now time to calc ela[psed time for scripted logging
        self.elapsed_time = time()

        # log the decision
        logging.info(decision_type)
        self.hivemind.design_decision = decision_type


    def high_energy_response(self):
        """
        Clear commands to interupt current gesture and moves on to new ones.
        """
        # self.drawbot.clear_commands()
        # self.drawbot.go_random_jump()
        high_energy_log = "Drawing High Energy random 3D"
        logging.info(high_energy_log)
        self.hivemind.design_decision = high_energy_log
        if self.XARM_CONNECTED:
            self.drawbot.go_random_3d()

    def terminate(self):
        """
        Smart collapse of all threads and comms.
        """
        print('TERMINATING robot and conducter')
        if self.drawbot:
            # self.drawbot.go_position_draw()
            # self.drawbot.go_position_one_two()
            # self.drawbot.home()
            self.drawbot.clear_commands()
            # if self.DOBOT_CONNECTED:
            #     self.drawbot.close()
            if self.XARM_CONNECTED:
                self.drawbot.set_fence_mode(False)
                self.drawbot.move_gohome()
                self.drawbot.disconnect()

    def rnd(self, power_of_command: int) -> int:
        """
        Returns a randomly generated positive or negative integer, influenced
        by the incoming power factor.
        """
        power_of_command = int(power_of_command)
        if power_of_command <= 0:
            power_of_command = 1
        pos = 1
        if random() >= 0.5:
            pos = -1
        result = (randrange(1, 5) + randrange(power_of_command)) * pos
        if result == 0:
            result = 1
        logging.debug(f'Rnd result = {result}')
        return result

    def scripted_move_clear_alarms(self):
        while self.hivemind.MASTER_RUNNING:
            self.drawbot.clear_alarms()
            sleep(0.1)

    def scripted_move(self):
        """
        Follows a pre-defined scripted. Bypasses all gen funcs
        """
        # print("====================================================== STARTED SCRIPTED TEST")

        sleep(0.455397367477417)
        self.drawbot.go_random_jump()
        sleep(0.10782599449157715)
        self.drawbot.random_pen()
        sleep(6.124422073364258)
        self.drawbot.arc2D(484.6731731508081, -254.91455764466286, 489.6731731508081, -254.91455764466286)
        sleep(0.3409392833709717)
        self.drawbot.dot
        sleep(0.2204124927520752)
        self.drawbot.draw_circle(0, 0)
        sleep(1.2121360301971436)
        self.drawbot.note_head(6)
        sleep(1.2131330966949463)
        self.drawbot.position_move_by(4, -2, 0, wait=True)
        sleep(0.7808210849761963)
        self.drawbot.go_draw(103.198, 104.198, False)
        sleep(0.5140390396118164)
        self.drawbot.note_head(5)
        sleep(0.10877561569213867)
        self.drawbot.go_draw(103.198, 11.433)
        sleep(0.2197401523590088)
        self.drawbot.note_head(8)
        sleep(0.22073698043823242)
        self.drawbot.position_move_by(2, -3, 0, wait=True)
        sleep(0.23477721214294434)
        self.drawbot.go_draw(102.198, 16.436)
        sleep(0.10884881019592285)
        self.drawbot.arc2D(105.198, 20.436, 99.198, 17.436)
        sleep(0.3255653381347656)
        self.drawbot.go_draw(99.197, 12.435)
        sleep(1.8530502319335938)
        self.drawbot.dot
        sleep(0.10836625099182129)
        self.drawbot.go_draw(96.186, 103.186, False)
        sleep(2.071302890777588)
        self.drawbot.note_head(1)
        sleep(0.3471360206604004)
        self.drawbot.go_random_jump()
        sleep(3.769630193710327)
        self.drawbot.note_head(4),
        sleep(3.6959636211395264)
        self.drawbot.draw_random_char(0.00062333984375)
        sleep(0.5642523765563965)
        self.drawbot.go_draw(295.644, 297.644, False)
        sleep(0.11554884910583496)
        self.drawbot.note_head(7)
        sleep(1.3097195625305176)
        self.drawbot.return_to_coord()
        sleep(6.172041893005371)
        self.drawbot.arc2D(101.198, 106.198, 100.198, 103.198)
        sleep(0.26216673851013184)
        self.drawbot.go_draw(-12.402, 245.535)
        sleep(0.11094522476196289)
        self.drawbot.random_pen()
        sleep(0.11087679862976074)
        self.drawbot.note_head(5)
        sleep(0.10885429382324219)
        self.drawbot.dot
        sleep(0.11252260208129883)
        self.drawbot.draw_circle(4, 0)
        sleep(0.1104118824005127)
        self.drawbot.go_random_jump()
        sleep(6.279728651046753)
        self.drawbot.dot
        sleep(0.2949187755584717)
        self.drawbot.draw_circle(6, 0)
        sleep(0.10984039306640625)
        self.drawbot.go_draw(33.85, 32.85, False)
        sleep(0.11085629463195801)
        self.drawbot.return_to_coord()
        sleep(1.9098687171936035)
        self.drawbot.note_head(6)
        sleep(0.12630677223205566)
        self.drawbot.go_random_jump()
        sleep(0.10935378074645996)
        self.drawbot.return_to_coord()
        sleep(0.10735774040222168)
        self.drawbot.go_draw(-465.4833989442373, 371.8050453848756)
        sleep(0.23509573936462402)
        self.drawbot.draw_random_char(11.42598795498198)
        sleep(0.11285066604614258)
        self.drawbot.return_to_coord()
        sleep(0.10645675659179688)
        self.drawbot.return_to_coord()
        sleep(0.10731101036071777)
        self.drawbot.random_pen()
        sleep(0.29814648628234863)
        self.drawbot.dot
        sleep(0.10831069946289062)
        self.drawbot.random_pen()
        sleep(0.3683357238769531)
        self.drawbot.squiggle(
            [(4, -7, 2), (-7, -4, 7), (6, -4, -2), (-6, -6, -6), (9, 3, -6), (-3, -9, 5), (4, 2, 6), (8, -3, 6)])
        sleep(0.10338068008422852)
        self.drawbot.draw_random_char(7.810420121020257)
        sleep(0.10780787467956543)
        self.drawbot.go_draw(81.465, 67.465, False)
        sleep(4.967336177825928)
        self.drawbot.draw_circle(6, 0)
        sleep(0.22868585586547852)
        self.drawbot.go_draw(84.464, 63.465999999999994)
        sleep(0.11284756660461426)
        self.drawbot.random_pen()
        sleep(6.724385976791382)
        self.drawbot.dot
        sleep(0.7321789264678955)
        self.drawbot.note_head(4)
        sleep(0.73317551612854)
        self.drawbot.position_move_by(3, 5, 0, wait=True)
        sleep(0.9818196296691895)
        self.drawbot.note_head(6)
        sleep(0.22842049598693848)
        self.drawbot.return_to_coord()
        sleep(0.11391139030456543)
        self.drawbot.random_pen()
        sleep(0.21562719345092773)
        self.drawbot.random_pen()
        sleep(0.6557724475860596)
        self.drawbot.random_pen()
        sleep(5.143335342407227)
        self.drawbot.dot
        sleep(0.22692584991455078)
        self.drawbot.random_pen()
        sleep(0.1102912425994873)
        self.drawbot.go_draw(99.92, 56.906)
        sleep(0.21850085258483887)
        self.drawbot.draw_circle(0, 1)
        sleep(3.6305763721466064)
        self.drawbot.dot
        sleep(1.7177717685699463)
        self.drawbot.return_to_coord()
        sleep(0.1153249740600586)
        self.drawbot.draw_random_char(0.0006138671875)
        sleep(8.78401517868042)
        self.drawbot.squiggle(
            [(1, -3, -2), (4, 3, 3), (2, 2, -1), (3, 1, -3), (1, 3, -3), (-2, -4, -2), (1, 4, -1), (2, 3, 1)])
        sleep(0.45129990577697754)
        self.drawbot.go_draw(63.215, -293.799)
        sleep(1.088390588760376)
        self.drawbot.go_draw(61.215, 66.215, False)
        sleep(1.2287876605987549)
        self.drawbot.arc2D(64.215, 65.215, 62.215, 65.215)
        sleep(0.11031961441040039)
        self.drawbot.go_draw(63.192, 66.19200000000001, False)
        sleep(0.1197214126586914)
        self.drawbot.go_draw(61.192, 67.19200000000001)
        sleep(0.5607945919036865)
        self.drawbot.random_pen()
        sleep(0.11025643348693848)
        self.drawbot.arc2D(59.844, -56.326, 65.844, -56.326)
        sleep(0.45227599143981934)
        self.drawbot.go_draw(63.755, -58.144)
        sleep(0.22180461883544922)
        self.drawbot.go_draw(62.755, -60.144)
        sleep(0.11115741729736328)
        self.drawbot.dot
        sleep(6.3114707469940186)
        self.drawbot.note_head(5)
        sleep(6.312467336654663)
        self.drawbot.position_move_by(-1, -2, 0, wait=True)
        sleep(0.23322391510009766)
        self.drawbot.return_to_coord()
        sleep(0.11198735237121582)
        self.drawbot.draw_circle(0, 1)
        sleep(2.1756813526153564)
        self.drawbot.note_head(7)
        sleep(0.2337045669555664)
        self.drawbot.arc2D(185.104, -142.488, 189.104, -148.488)
        sleep(2.7210793495178223)
        self.drawbot.dot
        sleep(0.45125365257263184)
        self.drawbot.random_pen()
        sleep(7.283308267593384)
        self.drawbot.arc2D(353.976, -180.334, 355.976, -183.334)
        sleep(1.5017340183258057)
        self.drawbot.go_draw(198.8293167607559, 194.8293167607559, False)
        sleep(0.10985970497131348)
        self.drawbot.go_draw(196.8293167607559, 190.8293167607559)
        sleep(0.10808038711547852)
        self.drawbot.go_draw(194.8293167607559, 194.8293167607559)
        sleep(0.22110366821289062)
        self.drawbot.go_draw(192.8293167607559, 196.8293167607559, False)
        sleep(0.11160898208618164)
        self.drawbot.go_random_jump()
        sleep(0.2158963680267334)
        self.drawbot.random_pen()
        sleep(0.10937952995300293)
        self.drawbot.random_pen()
        sleep(10.137719631195068)
        self.drawbot.arc2D(-144.62993360051632, -81.26317856554454, -146.62993360051632, -76.26317856554454)
        sleep(5.746857166290283)
        self.drawbot.dot
        sleep(1.2233166694641113)
        self.drawbot.note_head(1)
        sleep(1.2243123054504395)
        self.drawbot.position_move_by(-3, 1, 0, wait=True)
        sleep(0.6738414764404297)
        self.drawbot.draw_circle(0, 0)
        sleep(0.5458641052246094)
        self.drawbot.return_to_coord()
        sleep(0.1098790168762207)
        self.drawbot.go_draw(64.75916662674751, 63.75916662674752, False)
        sleep(10.461374044418335)
        self.drawbot.squiggle([(-4, -4, -4), (-2, 2, 1), (3, 2, -1)])
        sleep(0.3544900417327881)
        self.drawbot.random_pen()
        sleep(0.7637579441070557)
        self.drawbot.random_pen()
        sleep(2.4620800018310547)
        self.drawbot.dot
        sleep(0.24106502532958984)
        self.drawbot.return_to_coord()
        sleep(0.18549203872680664)
        self.drawbot.arc2D(55.75916662674752, -286.64614866249065, 64.75916662674751, -292.6461486624906)
        sleep(0.10300374031066895)
        self.drawbot.dot

        #############################
        # lasts 6 mins after this point
        #############################
        # sleep(0.10847997665405273)
        # self.drawbot.go_draw(289.305, 136.007)
        # sleep(0.11150097846984863)
        # self.drawbot.draw_random_char(4.306621704096169)
        # sleep(0.7271418571472168)
        # self.drawbot.note_head(7)
        # sleep(0.10751008987426758)
        # self.drawbot.random_pen()
        # sleep(0.1138005256652832)
        # self.drawbot.squiggle([(5, 6, 2), (3, -5, 4), (-3, 1, 5), (-4, -4, -2)])
        # sleep(0.2298126220703125)
        # self.drawbot.arc2D(262.736, 93.308, 269.736, 102.308)
        # sleep(0.11023449897766113)
        # self.drawbot.arc2D(275.455, 103.693, 274.455, 99.693)
        # sleep(0.12184596061706543)
        # self.drawbot.dot
        # sleep(0.1140127182006836)
        # self.drawbot.return_to_coord()
        # sleep(0.42867612838745117)
        # self.drawbot.dot
        # sleep(0.10119867324829102)
        # self.drawbot.go_draw(288.24, 290.24, False)
        # sleep(0.11142587661743164)
        # self.drawbot.note_head(6)
        # sleep(0.1277923583984375)
        # self.drawbot.note_head(5)
        # sleep(0.10446023941040039)
        # self.drawbot.go_draw(297.756, 295.756, False)
        # sleep(0.11000251770019531)
        # self.drawbot.return_to_coord()
        # sleep(0.11667037010192871)
        # self.drawbot.squiggle(
        #     [(5, 5, 2), (-3, 1, -3), (4, 3, -4), (-5, 4, 4), (-3, 6, -4), (2, -2, 2), (5, -4, -1), (2, -5, -3)])
        # sleep(0.10144352912902832)
        # self.drawbot.random_pen()
        # sleep(0.12680745124816895)
        # self.drawbot.draw_random_char(5.844714517616987)
        # sleep(0.10830950736999512)
        # self.drawbot.go_draw(291.689285482383, 82.14735725880848)
        # sleep(21.705406665802002)
        # self.drawbot.squiggle([(2, -4, -1), (-5, -4, -3), (1, -2, 4), (2, -6, 5), (-5, -2, 5), (-1, 6, 1)])
        # sleep(0.40122318267822266)
        # self.drawbot.note_head(3)
        # sleep(0.4022200107574463)
        # self.drawbot.position_move_by(1, -2, 0, wait=True)
        # sleep(0.8026628494262695)
        # self.drawbot.draw_random_char(0.000594140625)
        # sleep(0.5026524066925049)
        # self.drawbot.note_head(8)
        # sleep(0.11068892478942871)
        # self.drawbot.arc2D(-269.179, -66.312, -263.179, -69.312)
        # sleep(0.21979236602783203)
        # self.drawbot.go_random_jump()
        # sleep(0.23668551445007324)
        # self.drawbot.note_head(2)
        # sleep(0.23668551445007324)
        # self.drawbot.position_move_by(1, 2, 0, wait=True)
        # sleep(0.6305365562438965)
        # self.drawbot.squiggle([(-4, 1, 2), (4, 2, -3), (-3, 2, -4)])
        # sleep(0.32675600051879883)
        # self.drawbot.return_to_coord()
        # sleep(0.11125826835632324)
        # self.drawbot.draw_circle(0, 1)
        # sleep(0.10641288757324219)
        # self.drawbot.go_draw(-255.19099999999997, -259.191, False)
        # sleep(0.21921277046203613)
        # self.drawbot.go_draw(-262.191, -64.432)
        # sleep(0.6691162586212158)
        # self.drawbot.go_draw(-254.20600000000002, -64.788)
        # sleep(0.3311612606048584)
        # self.drawbot.squiggle([(-2, 4, -3), (-2, 4, -3), (-2, -3, 2), (2, 1, -3)])
        # sleep(0.2414262294769287)
        # self.drawbot.note_head(4)
        # sleep(0.2255251407623291)
        # self.drawbot.note_head(9)
        # sleep(0.11070942878723145)
        # self.drawbot.squiggle([(4, 3, -2), (3, -4, 1), (4, 2, -3), (4, 2, -2), (-2, 2, -4), (-4, 2, -3)])
        # sleep(0.29098939895629883)
        # self.drawbot.note_head(2)
        # sleep(0.29098939895629883)
        # self.drawbot.position_move_by(-2, -4, 0, wait=True)
        # sleep(0.657839298248291)
        # self.drawbot.draw_random_char(0.00092958984375)
        # sleep(0.225632905960083)
        # self.drawbot.go_draw(-239.776, -247.776, False)
        # sleep(0.21495342254638672)
        # self.drawbot.go_random_jump()
        # sleep(2.8896260261535645)
        # self.drawbot.note_head(5)
        # sleep(0.24572992324829102)
        # self.drawbot.return_to_coord()
        # sleep(0.11275005340576172)
        # self.drawbot.go_random_jump()
        # sleep(4.527878761291504)
        # self.drawbot.squiggle([(6, -2, 8), (4, 6, -3), (2, 7, 5), (8, -2, 4), (4, 7, 1)])
        # sleep(4.69010329246521)
        # self.drawbot.arc2D(260.427, 254.142, 262.427, 259.142)
        # sleep(0.5601630210876465)
        # self.drawbot.go_draw(171.82, 163.82, False)
        # sleep(23.530739545822144)
        # self.drawbot.note_head(9)
        # print("====================================================== END OF SCRIPTED TEST")
        self.doing_script = False
