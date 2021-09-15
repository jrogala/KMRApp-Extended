################################
# Kissmyrank In-Game Spotter App for Assetto Corsa
# Author: Brioche, Jimmy Rogala
# Version: 0.2a
# License: No warranty. Do whatever you like (:.
################################

# noinspection PyUnresolvedReferences
import ac
# noinspection PyUnresolvedReferences
import acsys
import sys
import os
import platform
import re
import time
import json
import traceback
# noinspection PyUnresolvedReferences
import encodings

if platform.architecture()[0] == "64bit":
    sys.path.insert(len(sys.path), 'apps/python/Kissmyrank/stdlib64')
else:
    sys.path.insert(len(sys.path), 'apps/python/Kissmyrank/stdlib')
os.environ['PATH'] = os.environ['PATH'] + ";."

import socket
import winsound

# Create DIR if not present
if not os.path.isdir("apps/python/Kissmyrank/config"):
    os.mkdir("apps/python/Kissmyrank/config")

try:
    # globals
    config = {
        "image_base_path": "apps/python/Kissmyrank/images/",
        "image_pack": "default",
        "sound_base_path": "apps/python/Kissmyrank/sounds/",
        "sound_pack": "default",
        "link": {
            "on": True
        },
        "flags": {
            "on": 1,
            "layout": "horizontal",
            "width": 360,  # 3 x single flag width+ 2 x spacing
            "height": 100,  # single flag height
            "spacing": 30  # space between two flags
        },
        "messages": {
            "on": 1,
            "width": 1224,
            "font_size": 16,
            "line_height": 24,
            "spacing": 9
        },
        "UI": {
            "show": True
        },
        "config_file_path": "apps/python/Kissmyrank/config/config.json",
    }


    def configLoad():
        global config
        try:
            with open(config["config_file_path"], 'r') as config_file:
                content = config_file.read()
            if content:
                temp_config = json.loads(content)
                for k, v in temp_config.items():
                    try:
                        config[k].update(v)
                    except:
                        config[k] = v
        except:
            ac.log("Kissmyrank Error:" + str(traceback.format_exc()))
            pass


    configLoad()
    applink = {
        "app_id": "Kissmyrank",
        "connected": 0,
        "ip": "",
        "port": 0,
        "token": "",
        "sock": 0,
        "chat_fail_counter": 99,
        "position": 0
    }
    # noinspection PyDictCreation
    kissmyrank = {
        "timers": [0, 0, 0],
        "started": 0,
        "fails": 0,
        "heartbeat": 0,
        "link": {
            "on": config["link"]["on"],
            "width": 0,
            "height": 0
        },
        "flags": {
            "on": config["flags"]["on"],
            "controls": {  # slot 0 left (no timer), slot 1 center (with timer), slot 2 right (no timer)
                "vsc": {
                    "path": "vsc.png",
                    "slot": 0
                },
                "vsc10": {
                    "path": "vsc10.png",
                    "slot": 0
                },
                "vsc3": {
                    "path": "vsc3.png",
                    "slot": 0
                },
                "vsc2": {
                    "path": "vsc2.png",
                    "slot": 0
                },
                "vsc1": {
                    "path": "vsc1.png",
                    "slot": 0
                },
                "penalty": {
                    "path": "penalty.png",
                    "slot": 1
                },
                "damage_cars": {
                    "path": "warning.png",
                    "slot": 1
                },
                "damage_env": {
                    "path": "warning.png",
                    "slot": 1
                },
                "speeding": {
                    "path": "slowdown.png",
                    "slot": 1
                },
                "snail": {
                    "path": "snail1.png",
                    "slot": 1
                },
                "formation_lap": {
                    "path": "formationlap.png",
                    "slot": 0
                },
                "speed_80": {
                    "path": "80limit.png",
                    "slot": 2
                },
                "speed_100": {
                    "path": "100limit.png",
                    "slot": 2
                },
                "speed_120": {
                    "path": "120limit.png",
                    "slot": 2
                },
                "speed_150": {
                    "path": "150limit.png",
                    "slot": 2
                },
                "speed_vsc": {
                    "path": "speedvsc.png",
                    "slot": 2
                },
                "speed_fl": {
                    "path": "speedfl.png",
                    "slot": 2
                },
                "black_flag": {
                    "path": "black.png",
                    "slot": 2
                },
                "yellow_flag": {
                    "path": "yellow.png",
                    "slot": 2
                },
                "blue_flag": {
                    "path": "blue.png",
                    "slot": 1
                },
                "blue_yellow": {
                    "path": "blueyellow.png",
                    "slot": 1
                },
                "red_flag": {
                    "path": "red.png",
                    "slot": 1
                },
                "green_flag": {
                    "path": "green.png",
                    "slot": 1
                },
                "dt_penalty": {
                    "path": "dtblack.png",
                    "slot": 2
                },
                "dt_penaltynow": {
                    "path": "dtblack2.png",
                    "slot": 2
                },
                "dt_penalty_next_race": {
                    "path": "dtpenalty.png",
                    "slot": 1
                },
                "pit_now": {
                    "path": "pitnow2.png",
                    "slot": 1
                },
                "no_overtake": {
                    "path": "noovertake.png",
                    "slot": 1
                },
                "warning": {
                    "path": "penalty.png",
                    "slot": 1
                },
                "money_penalty": {
                    "path": "penalty.png",
                    "slot": 1
                },
                "noparking": {
                    "path": "noparking.png",
                    "slot": 1
                }
            },
            "active": [[], [], []],
            "last_cycle": time.time()
        },
        "messages": {
            "on": config["messages"]["on"],
            "font": "Tw Cen MT Condensed",
            "lines": 9,
            "controls": {},
            "used_slots": [0, 1]
        },
        "settings": {
            "on": 0,
            "width": 300,
            "height": 650,
            "controls": {},
            "cursor": 33,
            "need_updating": []
        },
        "event_map": {
            # flags [flag1, flag2], sound, shows [show_flag1, show_flag2, show_text_slot0, show_text_slot1], text slot, seconds
            # "welcome_driving_stats": "Driven Distance: %s, Crashes: %d (per 100km: %s).",
            # "welcome_personal_best": "Your Personal Best: %s, Server Best: %s.",
            # "track_record_yours": "the track record is yours",
            # "no_time_set": "No time set",
            # "by": "by",
            # "welcome_lap_time_challenge": "You are level %d in the laptime challenge (next time to beat: %s, reward: %s).",
            # "welcome_winning_stats": "Wins: %d, Podiums: %d, Poles: %d, Fastest Laps: %d, Driving Infractions: %d (per 100km: %s).",
            # "welcome_money": "You have %s in your Account (rank: %s).",
            # "new": "new",
            # "welcome_get_help": "Type %s for a list of available commands.",
            # "welcome_race_control": "Live Race Control running on: http://%s/race_control",
            # "formation_lap_rules": "Rolling start. Formation Lap rules:",
            "formation_lap_speed_limit": [["formation_lap", "speed_fl"], "notify.wav", [1, 1], -1, 2],
            "formation_lap_speed_limit_80km/h": [["formation_lap", "speed_80"], "notify.wav", [1, 1], -1, 2],
            "formation_lap_speed_limit_100km/h": [["formation_lap", "speed_100"], "notify.wav", [1, 1], -1, 2],
            "formation_lap_speed_limit_120km/h": [["formation_lap", "speed_120"], "notify.wav", [1, 1], -1, 2],
            "formation_lap_speed_limit_150km/h": [["formation_lap", "speed_150"], "notify.wav", [1, 1], -1, 2],
            # "formation_lap_do_not_overtake": "- do not overtake before the Green Flag signal",
            # "formation_lap_might_overtake_1": "- you might overtake if the car ahead is farther than %s from the previous one",
            # "formation_lap_might_overtake_2": "- you might overtake if the car is ahead farther than %s and slower than %s",
            "virtual_safety_car_deployed": [["vsc", "speed_vsc"], "notify.wav", [1, 1, 1], 0, ],
            "virtual_safety_car_deployed_80km/h": [["vsc", "speed_80"], "notify.wav", [1, 1, 1], 0],
            "virtual_safety_car_deployed_100km/h": [["vsc", "speed_100"], "notify.wav", [1, 1, 1], 0],
            "virtual_safety_car_deployed_120km/h": [["vsc", "speed_120"], "notify.wav", [1, 1, 1], 0],
            "virtual_safety_car_deployed_150km/h": [["vsc", "speed_150"], "notify.wav", [1, 1, 1], 0],
            # "qualify_top_3_prize": "Congratulations: +%s for qualifying in the %s position (you now have %s).",
            # "race_pay": "Reward: you have been paid %s for finishing %s.",
            # "race_no_pay": "Sorry but there is no prize for the %s position this time.",
            # "race_fastest_lap_prize": "Reward: you have been paid %s for the fastest lap of the race.",
            # "race_clean_gain_reward": "Reward: your sponsors are impressed. They paid you additional %s for your great performance.",
            # "race_position_overview_a": "Start Pos: %s, Finish Pos: %s (%s).",
            # "clean_gain": "clean gain",
            # "collisions": "collisions",
            # "race_position_overview_b": "Did not qualify. Finish Pos: %s (collisions: %d).",
            # "session_balance_overview": "Your Balance (last session: %s, you now have %s).",
            # "race_entry_fee": "Cost: you just paid %s to enter the race (you now have %s). Drive to the end to get the prize!",
            # "laptime_challenge_reward": "Reward: you earned %s for reaching level %d (next time to beat: %s, reward: %s).",
            # "race_over_position": "Race over. %s position.",
            # "towing_cost": "Cost: you just paid %s to tow your car back to the pits (distance: %s, you now have %s).",
            "lapped_warning": [["blue_flag"], "notify.wav", [1], -1, 8],
            "hotlap_warning": [["blue_yellow"], "notify.wav", [1], -1, 8],
            "damage_between_cars_notification": [["damage_cars"], "notify.wav", [1], -1, 10],
            "damage_with_environment_notification": [["damage_env"], "notify.wav", [1], -1, 10],
            # "kmr_money_output": "You now have %s (rank: %s).",
            # "kmr_level_output": "You are level %d in the laptime challenge (next time to beat: %s, reward: %s).",
            # "available_commands": "Available commands:",
            # "kmr_rules_help": "%s: shows the server rules",
            # "kmr_leaderboard_help": "%s: shows the fastest times for the car you are driving",
            # "kmr_level_help": "%s: shows your level in the laptime challenge",
            # "kmr_best_help": "%s: shows your personal best for the car you are driving",
            # "kmr_money_help": "%s: shows how much %s you have",
            # "money": "money",
            # "points": "points",
            # "kmr_next_track_help": "%s: shows the next track in the server rotation",
            # "kmr_vote_track_help": "%s: vote for track change",
            # "kmr_stats_help": "%s: shows your driving stats",
            # "kmr_toggle_notifications_help": "%s: toggles driving notifications (rules still apply)",
            # "best_times_for_car": "Best Times for %s:",
            # "no_times_for_car": "There are no times recorded for this car. Jump in the car and make one.",
            # "kmr_best_output": "Your Personal Best with %s is %s%s.",
            # "rank": "rank",
            # "server_best": "server best",
            # "you_have_no_time_yet": "You haven't set a time yet. Jump in the car and set one.",
            # "kmr_next_track_output": "The next track is %s.",
            # "kmr_rules_output_1": "Make room for hotlapping cars during your quali outlap.",
            # "kmr_rules_output_2": "Respect blue flags during the race and make room if you're lapped.",
            # "kmr_rules_output_3": "Cars are expensive. Collisions will cost you %s for repairs.",
            # "kmr_rules_output_4": "If you go broke (less than %s) you will be kicked. Finish races and improve your laptimes to earn %s.",
            # "kmr_rules_output_5": "Keep it between the white lines. Rejoin track at %s max. Enter pits at %s max. Do not cross the pit exit line.",
            # "kmr_stats_output_1": "Driven Distance: %s, Crashes: %d (crashes per 100km: %s).",
            # "time_singular": "time",
            # "time_plural": "times",
            # "you_have_no_stats": "No stats to show yet. Please drive a bit more.",
            # "kmr_toggle_notifications_output": "Driving Notifications %s.",
            # "enabled": "enabled",
            # "disabled": "disabled",
            # "kmr_vote_track_output_1": "You can vote for one of the following tracks:",
            # "kmr_vote_track_output_2": "Type %s to cast your vote (e.g. %s).",
            # "already_voted": "You already casted your vote.",
            # "track_voting_not_allowed_now": "Track voting is only allowed during practice and qualify sessions.",
            # "new_personal_best": "New Personal Best: %s (%s).",
            # "all_times_fastest_lap_prize": "Reward: %s for setting the fastest lap of all times (you now have %s).",
            "virtual_safety_car_ending_in_10s": [["vsc10"], "notify.wav", [1], 0],
            "virtual_safety_car_ending_in_3s": [["vsc3"], "notify.wav", [1], 0],
            "virtual_safety_car_ending_in_2s": [["vsc2"], "notify.wav", [1], 0],
            "virtual_safety_car_ending_in_1s": [["vsc1"], "notify.wav", [1], 0],
            "virtual_safety_car_ended": [
                ["vsc1", "green_flag", "speed_80", "speed_100", "speed_120", "speed_150", "speed_vsc"], "notify.wav",
                [0, 1, 0, 0, 0, 0, 0, 0], -1, 10],
            # "track_rotation_in_30s": "The track will rotate in 30s (next track: %s).",
            # "track_rotation_in_20s": "The track will rotate in 20s (download the Kissmyrank AC Multiplayer Launcher Mod if you wish to auto-reconnect).",
            # "track_rotation_in_10s": "The track will rotate in 10s (you will now be booted for track rotation).",
            # "kicked_notification": "Kicked %s %s.",
            # "temporary_ban_broadcast": "%s (GUID: %s) is now banned for %s.",
            # "minute_singular": "minute",
            # "minute_plural": "minutes",
            # "formation_lap_start": [["formation_lap"], "notify.wav", [1, 1], -1, 8],
            "race_start": [["green_flag"], "notify.wav", [1], -1, 5],
            # "not_enough_drivers_to_race": "Minimum %d drivers are required to race. Moving to qualify.",
            # "race_start_prize_broadcast": "Race direction has collected a total competition prize of %s from drivers and sponsors (winner gets %s).",
            # "race_fastest_lap_broadcast": "%s set the fastest lap of the race: %s (lap: %d, %s).",
            # "race_winner_broadcast": "%s won the race!",
            # "race_second_broadcast": "%s is 2nd!",
            # "race_third_broadcast": "%s is 3rd!",
            "rolling_race_start": [["formation_lap", "green_flag"], "notify.wav", [0, 1], -1, 5],
            # "pole_position_broadcast": "%s is in pole position with %s (%s)!",
            "rolling_start_speed_limit_off": [
                ["formation_lap", "speed_80", "speed_100", "speed_120", "speed_150", "speed_vsc"], "notify.wav",
                [1, 0, 0, 0, 0, 0], -1, 8],
            # "first_blood_broadcast": "Penalty: %s %s for being involved in the first collisions of the race.",
            "automatic_race_restart_broadcast": [["red_flag"], "notify.wav", [1], -1, 6],
            # "driver_vote_broadcast": "%s voted to change the track to %s (%d of %d required).",
            # "track_change_vote_ends_in_30s": "Track Change Vote will end in 30 seconds. Cast your vote with the %s command before it's too late!",
            # "track_vote_result_broadcast": "%s has won the vote (%d out of %d).",
            # "track_vote_cancelled": "Track Change Vote cancelled from console.",
            # "all_times_fastest_lap_broadcast": "%s set the fastest lap of all times: %s (%s).",
            # "race_control_no_further_action": "Race control: no further action required for %d.",
            # "race_control_cancelled_drive_through": "Race Control: race director cancelled %s's drive-through penalty for event %d (%s).",
            # "race_control_temporary_banned_guid": "Race Control: race director banned GUID %s for %s minutes for event %d (%s).",
            # "race_control_inflicted_money_penalty": "Race Control: race director inflicted %s a %s money penalty for event %d (%s).",
            # "race_control_inflicted_points_penalty": "Race Control: race director inflicted %s a %s point penalty for event %d (%s).",
            # "race_control_set_points_penalty": "Race Control: race director set %s's points penalty for event %d to %s (%s).",
            # "race_control_set_money_penalty": "Race Control: race director set %s's money penalty for event %d to %s (%s).",
            # "race_control_confirmed_points_penalty": "Race Control: race director confirmed %s's points penalty for event %d to %s (%s).",
            # "race_control_confirmed_money_penalty": "Race Control: race director confirmed %s's money penalty for event %d to %s (%s).",
            # "race_control_cancelled_temporary_ban": "Race Control: race director cancelled GUID %s temporary ban for event %d (%s).",
            # "race_control_collision_under_investigation": "Race Control: Collision between %s and %s is under investigation by the race director (id: %d, %s).",
            # "race_control_cut_under_investigation": "Race Control: %s's behavior on track is under investigation by the race director (event id: %d, %s).",
            # "race_control_overtake_under_investigation": "Race Control: %s's overtake is under review by the race director (event id: %d, %s).",
            # "race_control_cancelled_points_penalty": "Race Control: race director cancelled %s's point penalty for event %d (%s).",
            # "race_control_cancelled_money_penalty": "Race Control: race director cancelled %s's money penalty for event %d (%s).",
            # "recording_aborted_speed_too_high": "Warning: speed too high. Recording aborted. Please start over.",
            "overtaking_not_permitted_now": [["no_overtake"], "notify.wav", [1], -1, 8],
            # "saving_recording": "Saving %s.",
            # "starting_recording": "Starting %s recording.",
            "penalties_cleared": [["dt_penalty"], "notify.wav", [0, 1, 0], -1, 10],
            "cutline_laptime_invalidated_warning": [["warning"], "notify.wav", [1], -1, 10],
            "track_boundary_laptime_invalidated_warning": [["warning"], "notify.wav", [1], -1, 10],
            "track_boundary_laptime_invalidated_warning_do_not_improve_your_laptime": [["warning", "speeding"],
                                                                                       "notify.wav", [1, 1], -1, 10],
            "track_boundary_laptime_invalidated_warning_pass_through_pits": [["warning", "pit_now"],
                                                                             "notify.wav", [1, 1], -1, 10],
            "speed_limit_warning_virtual_safety_car": [["speeding"], "notify.wav", [1], -1, 2],
            "speed_limit_warning_formation_lap": [["speeding"], "notify.wav", [1], -1, 2],
            # "virtual_safety_car": "Virtual Safety Car",
            # "formation_lap": "Formation Lap",
            "min_speed_warning_virtual_safety_car": [["snail"], "notify.wav", [1], -1, 2],
            "min_speed_warning_formation_lap": [["snail"], "notify.wav", [1], -1, 2],
            "drive_through_aborted_warning": [["warning"], "notify.wav", [1], -1, 10],
            "penalty_drive_through_this_lap": [["dt_penaltynow"], "notify.wav", [1, 1, 1], 1],
            "penalty_drive_through_within_laps": [["dt_penalty"], "notify.wav", [1, 1, 1], 1],
            # "lap_singular": "lap",
            # "lap_plural": "laps",
            "money_penalty": [["penalty"], "notify.wav", [1], -1, 10],
            "penalty_warning": [["penalty"], "notify.wav", [1], -1, 10],
            "ping_high_warning": [["warning"], "notify.wav", [1], -1, 10],
            "cpu_clock_time_check_warning": [["warning"], "notify.wav", [1], -1, 10],
            "clear_drive_through_this_lap_warning": [["warning"], "notify.wav", [1, 1, 1], 1, 10],
            "clear_drive_through_within_laps_warning": [["warning"], "notify.wav", [1, 1, 1], 1, 10],
            # "chat_admin_logged_in": "You are logged in as Kissmyrank Admin. Type /kmr command to run a Kissmyrank Console command.",
            # "track_boundary_recording_tip": "Please place your car before the start/finish line on the %s track boundary (the farthest drivers should be allowed to drive). Then drive a full lap on the boundary while being as precise as possible (recording will be aborted if you speed over %s).",
            # "left": "left",
            # "right": "right",
            # "track_boundary_include_exclude_tip": "Please place your car on the %s side of the track in the first point of the area where boundary cuts should be %s. Then slowly drive to the end of the area and run the %s command (max speed: %s).",
            # "considered": "considered",
            # "ignored": "ignored",
            # "pit_boundary_recording_tip": "Please place your car on the first point of the %s pit boundary. Then slowly drive to the end of the %s pit boundary (do not reverse!) and run the %s command (max speed: %s).",
            # "accessory_boundary_recording_tip": "Please place your car on the first point of the %s accessory area boundary that you wish to define. Then slowly drive to the end of the %s accessory boundary (do not reverse!) and run the %s command (max speed: %s).",
            # "saving_accessory_boundary_recording": "Saving %s for %s.",
            # "for_track_rotation": "for track rotation",
            # "for_running_out_of_money": "for running out of money",
            # "for_not_meeting_driving_standards": "for not meeting the minimum driving standards",
            # "for_crashing_too_much": "for crashing too much",
            # "because_of_high_ping": "because of high ping (average: %dms)",
            # "because_of_unstable_ping": "because of unstable ping (deviation: %dms)",
            # "for_not_clearing_drive_through": "for not clearing the drive-through penalty",
            # "from_console": "from console",
            # "because_slot_reserved": "because the slot is reserved for another driver",
            # "for_violating_overtake_restriction": "for violating the overtake restriction",
            # "for_too_many_collisions": "for being involved in too many collisions during this session",
            # "for_speeding_during_virtual_safety_car": "for speeding during the Virtual Safety Car",
            # "for_speeding_during_formation_lap": "for speeding during the Formation Lap",
            # "for_slowing_during_virtual_safety_car": "for slowing down too much during the Virtual Safety Car",
            # "for_slowing_during_formation_lap": "for slowing down too much during the Formation Lap",
            # "for_reversing_too_much": "for driving in reverse gear for %s",
            # "because_times_do_not_match_server_clock": "because your times do not match the server's. Please check your CPU clock.",
            # "for_pit_lane_speeding": "for pit lane speeding (speed: %s, speed limit: %s)",
            # "for_crossing_pit_exit_line": "for crossing the pit exit line",
            # "for_crossing": "for crossing %s",
            # "the left track boundary": "the left track boundary",
            # "the right track boundary": "the right track boundary",
            # "for_speeding_on": "for speeding on %s (speed: %s, speed limit: %s)",
            # "for_rejoining_track_high_speed": "for rejoining the track at high speed (speed: %s, speed limit: %s)",
            # "for_cut_line_cut": "for cutting %s%s",
            # "speed": "speed",
            # "speed_limit": "speed limit",
            # "for_reaching_infraction_limit": "for reaching the infraction limit",
            # "for_ignoring_blue_flags": "for ignoring the blue flags",
            # "for_disturbing_another_driver_hotlap": "for disturbing another driver hotlap",
            # "for_first_blood": "for being involved in the first collisions of the race",
            # "for_lapping_car_collision": "for colliding with a car that was lapping you",
            # "for_hotlapping_car_collision": "for colliding with a car in the hotlap",
            # "language_changed_to": "Language changed to %s.",
            # "language_not_available": "The specified language is not available (available languages: %s). Please help translating Kissmyrank to your language on RaceDepartment or the Assetto Corsa forum.",
            # "kmr_language_help": "%s: changes the Kissmyrank language to it = Italian (available languages: %s)",
            # "kmr_language_list_output": "Available languages: %s (type %s to change)",
            # "do_not_improve_your_laptime": "Do not improve your laptime this lap.",
            "penalty_drive_through_at_next_race": [["dt_penalty_next_race"], "notify.wav", [1], -1, 10],
            # "for_parking_the_car_near_track": "for parking the car in proximity of the track",
            "parked_car_near_track_warning": [["noparking"], "notify.wav", [1], -1, 6],
        },
        "event_submap": {  # 1 appends _first_%_argument of the en.json line
            "formation_lap_speed_limit": [1],
            "virtual_safety_car_deployed": [2],
            "track_boundary_laptime_invalidated_warning": [1]
        },
        "event_queue": []
    }

    t1 = """def onFlagLayoutSelect_%s(*args):
            global config, kissmyrank
            config["flags"]["layout"] = "%s"
            flagsLayoutHighlightUpdate()
            temp = config["flags"]["width"]
            config["flags"]["width"] = config["flags"]["height"]
            config["flags"]["height"] = temp
            updateFlagsSize()
            configSave()
            positionFlags()
            kissmyrank["settings"]["need_updating"].append("width")
            kissmyrank["settings"]["need_updating"].append("height")"""

    exec(t1 % ("horizontal", "horizontal"))
    exec(t1 % ("vertical", "vertical"))

    t2 = """def onImagePackSelect_%s(*args):
            global config, kissmyrank
            config["image_pack"] = "%s"
            # imagePackHighlightUpdate()
            configSave()"""

    kissmyrank["image_packs"] = []
    for d in os.listdir(config["image_base_path"]):
        if os.path.isdir(os.path.join(config["image_base_path"], d)):
            # noinspection PyTypeChecker
            kissmyrank["image_packs"].append(d)
    for im_p in kissmyrank["image_packs"]:
        exec(t2 % (im_p, im_p))

    t3 = """def onSoundPackSelect_%s(*args):
                global config, kissmyrank
                config["sound_pack"] = "%s"
                soundPackHighlightUpdate()
                configSave()"""
    kissmyrank["sound_packs"] = ["mute"]
    for d in os.listdir(config["sound_base_path"]):
        if os.path.isdir(os.path.join(config["sound_base_path"], d)):
            # noinspection PyTypeChecker
            kissmyrank["sound_packs"].append(d)
    for so_p in kissmyrank["sound_packs"]:
        exec(t3 % (so_p, so_p))


    # noinspection PyUnusedLocal
    def acMain(ac_version):
        global kissmyrank, config

        ac.log("Kissmyrank: setting up Kissmyrank Settings App.")
        kissmyrank["settings"]["id"] = ac.newApp("Kissmyrank Settings")
        ac.setTitle(kissmyrank["settings"]["id"], "Kissmyrank Settings")
        ac.drawBorder(kissmyrank["settings"]["id"], 0)
        ac.setSize(kissmyrank["settings"]["id"], kissmyrank["settings"]["width"], kissmyrank["settings"]["height"])
        ac.setVisible(kissmyrank["settings"]["id"], kissmyrank["settings"]["on"])
        ac.addOnAppActivatedListener(kissmyrank["settings"]["id"], onSettingsOn)
        ac.addOnAppDismissedListener(kissmyrank["settings"]["id"], onSettingsOff)
        # kissmyrank["settings"]["controls"]["image_pack_select_label"] = {}
        # kissmyrank["settings"]["controls"]["image_pack_select_label"]["id"] = ac.addLabel(kissmyrank["settings"]["id"],
        #                                                                                   "Image Pack:")
        # ac.setPosition(kissmyrank["settings"]["controls"]["image_pack_select_label"]["id"], 3,
        #                kissmyrank["settings"]["cursor"])
        # settingsNextLine()
        # ac.setSize(kissmyrank["settings"]["controls"]["image_pack_select_label"]["id"], kissmyrank["settings"]["width"],
        #            30)
        # kissmyrank["settings"]["controls"]["image_packs"] = {}
        # REMOVED IMAGE PACK
        # try:
        #     # noinspection PyTypeChecker
        #     image_packs = kissmyrank["image_packs"]
        #     for image_pack in image_packs:
        #         kissmyrank["settings"]["controls"]["image_packs"][image_pack] = {}
        #         kissmyrank["settings"]["controls"]["image_packs"][image_pack]["id"] = ac.addButton(
        #             kissmyrank["settings"]["id"], image_pack)
        #         ac.setPosition(kissmyrank["settings"]["controls"]["image_packs"][image_pack]["id"],
        #                        3, kissmyrank["settings"]["cursor"])
        #         settingsNextLine()
        #         ac.setSize(kissmyrank["settings"]["controls"]["image_packs"][image_pack]["id"],
        #                    kissmyrank["settings"]["width"] - 6,
        #                    24)
        #         ac.drawBorder(kissmyrank["settings"]["controls"]["image_packs"][image_pack]["id"], 0)
        #         ac.setVisible(kissmyrank["settings"]["controls"]["image_packs"][image_pack]["id"], 1)
        #         imagePackHighlight(image_pack)
        #         # noinspection PyUnresolvedReferences
        #         ac.addOnClickedListener(kissmyrank["settings"]["controls"]["image_packs"][image_pack]["id"],
        #                                 eval("onImagePackSelect_" + image_pack))
        # except:
        #     pass
        # settingsNextLine(6)
        kissmyrank["settings"]["controls"]["flags_layout_select_label"] = {}
        kissmyrank["settings"]["controls"]["flags_layout_select_label"]["id"] = ac.addLabel(
            kissmyrank["settings"]["id"],
            "Flags Layout:")
        ac.setPosition(kissmyrank["settings"]["controls"]["flags_layout_select_label"]["id"], 3,
                       kissmyrank["settings"]["cursor"])
        settingsNextLine()
        kissmyrank["settings"]["controls"]["flags_layouts"] = {}
        try:
            # noinspection PyTypeChecker
            flag_layouts = ["horizontal", "vertical"]
            for flag_layout in flag_layouts:
                kissmyrank["settings"]["controls"]["flags_layouts"][flag_layout] = {}
                kissmyrank["settings"]["controls"]["flags_layouts"][flag_layout]["id"] = ac.addButton(
                    kissmyrank["settings"]["id"], flag_layout)
                ac.setPosition(kissmyrank["settings"]["controls"]["flags_layouts"][flag_layout]["id"],
                               3, kissmyrank["settings"]["cursor"])
                settingsNextLine()
                ac.setSize(kissmyrank["settings"]["controls"]["flags_layouts"][flag_layout]["id"],
                           kissmyrank["settings"]["width"] - 6,
                           24)
                ac.drawBorder(kissmyrank["settings"]["controls"]["flags_layouts"][flag_layout]["id"], 0)
                ac.setVisible(kissmyrank["settings"]["controls"]["flags_layouts"][flag_layout]["id"], 1)
                flagsLayoutHighlight(flag_layout)
                # noinspection PyUnresolvedReferences
                # noinspection PyUnresolvedReferences
                ac.addOnClickedListener(kissmyrank["settings"]["controls"]["flags_layouts"][flag_layout]["id"],
                                        eval("onFlagLayoutSelect_" + flag_layout))
        except:
            pass
        settingsNextLine(6)
        # addSettingsTextInput("flags_width", "Flags Width:", onFlagsWidthChange)
        # settingsNextLine(30)
        # addSettingsTextInput("flags_height", "Flags Height:", onFlagsHeightChange)
        # settingsNextLine(30)
        # addSettingsTextInput("flags_spacing", "Flags Spacing:", onFlagsSpacingChange)
        # settingsNextLine(30)
        # addSettingsTextInput("messages_width", "Messages Width:", onMessagesWidthChange)
        # settingsNextLine(30)
        # addSettingsTextInput("messages_font_size", "Messages Font Size:", onMessagesFontSizeChange)
        # settingsNextLine(30)
        # addSettingsTextInput("messages_line_height", "Messages Line Height:", onMessagesLineHeightChange)
        # settingsNextLine(30)
        # addSettingsTextInput("messages_spacing", "Messages Spacing:", onMessagesSpacingChange)
        # settingsNextLine(30)
        addSettingsBoxInput("messages_ui", "Show UI:", onUISettingChange)
        settingsNextLine(30)
        addSettingsBoxInput("connect_KMR", "Connect KMR:", onKMRConnectChange)
        settingsNextLine(30)
        kissmyrank["settings"]["controls"]["sound_pack_select_label"] = {}
        kissmyrank["settings"]["controls"]["sound_pack_select_label"]["id"] = ac.addLabel(kissmyrank["settings"]["id"],
                                                                                          "Sound Pack:")
        ac.setPosition(kissmyrank["settings"]["controls"]["sound_pack_select_label"]["id"], 3,
                       kissmyrank["settings"]["cursor"])
        settingsNextLine()
        ac.setSize(kissmyrank["settings"]["controls"]["sound_pack_select_label"]["id"], kissmyrank["settings"]["width"],
                   30)
        kissmyrank["settings"]["controls"]["sound_packs"] = {}
        try:
            # noinspection PyTypeChecker
            sound_packs = kissmyrank["sound_packs"]
            for sound_pack in sound_packs:
                kissmyrank["settings"]["controls"]["sound_packs"][sound_pack] = {}
                kissmyrank["settings"]["controls"]["sound_packs"][sound_pack]["id"] = ac.addButton(
                    kissmyrank["settings"]["id"], sound_pack)
                ac.setPosition(kissmyrank["settings"]["controls"]["sound_packs"][sound_pack]["id"],
                               3, kissmyrank["settings"]["cursor"])
                settingsNextLine()
                ac.setSize(kissmyrank["settings"]["controls"]["sound_packs"][sound_pack]["id"],
                           kissmyrank["settings"]["width"] - 6,
                           24)
                ac.drawBorder(kissmyrank["settings"]["controls"]["sound_packs"][sound_pack]["id"], 0)
                ac.setVisible(kissmyrank["settings"]["controls"]["sound_packs"][sound_pack]["id"], 1)
                soundPackHighlight(sound_pack)
                # noinspection PyUnresolvedReferences
                ac.addOnClickedListener(kissmyrank["settings"]["controls"]["sound_packs"][sound_pack]["id"],
                                        eval("onSoundPackSelect_" + sound_pack))
        except:
            pass

        # ac.log("Kissmyrank: setting up Kissmyrank Link App.")
        # kissmyrank["link"]["id"] = ac.newApp("Kissmyrank Link")
        # ac.setTitle(kissmyrank["link"]["id"], "")
        # ac.setIconPosition(kissmyrank["link"]["id"], 0, -6000)
        # ac.setSize(kissmyrank["link"]["id"], kissmyrank["link"]["width"], kissmyrank["link"]["height"])
        # ac.drawBorder(kissmyrank["link"]["id"], 0)
        # ac.setBackgroundColor(kissmyrank["link"]["id"], 0, 0, 0)
        # ac.setBackgroundOpacity(kissmyrank["link"]["id"], 0)
        # ac.setVisible(kissmyrank["link"]["id"], kissmyrank["link"]["on"])
        # ac.addOnAppActivatedListener(kissmyrank["link"]["id"], onLinkOn)
        # ac.addOnAppDismissedListener(kissmyrank["link"]["id"], onLinkOff)
        # # ac.addRenderCallback(ac_kissmyrank["link"]["id"], onRender)
        # ac.addOnChatMessageListener(kissmyrank["link"]["id"], onMessage)

        ac.log("Kissmyrank: setting up Kissmyrank Flags App.")
        kissmyrank["flags"]["id"] = ac.newApp("Kissmyrank Flags")
        ac.setTitle(kissmyrank["flags"]["id"], "Flags")
        ac.drawBorder(kissmyrank["flags"]["id"], 1)
        ac.setIconPosition(kissmyrank["flags"]["id"], 0, -6000)
        updateFlagsSize()
        ac.setBackgroundColor(kissmyrank["flags"]["id"], 0, 0, 0)
        ac.setBackgroundOpacity(kissmyrank["flags"]["id"], 0)
        ac.setVisible(kissmyrank["flags"]["id"], kissmyrank["flags"]["on"])
        ac.addOnAppActivatedListener(kissmyrank["flags"]["id"], onFlagsOn)
        ac.addOnAppDismissedListener(kissmyrank["flags"]["id"], onFlagsOff)
        # add flag controls
        for id_, flag in kissmyrank["flags"]["controls"].items():
            kissmyrank["flags"]["controls"][id_]["id"] = ac.addButton(kissmyrank["flags"]["id"], "")
            positionFlag(id_)
            ac.drawBorder(kissmyrank["flags"]["controls"][id_]["id"], 0)
            ac.setVisible(kissmyrank["flags"]["controls"][id_]["id"], 0)
            ac.setBackgroundOpacity(kissmyrank["flags"]["controls"][id_]["id"], 0)
            ac.setBackgroundTexture(kissmyrank["flags"]["controls"][id_]["id"],
                                    config["image_base_path"] + config["image_pack"] + "/" +
                                    kissmyrank["flags"]["controls"][id_]["path"])
            ac.setVisible(kissmyrank["flags"]["controls"][id_]["id"], 0)

        ac.log("Kissmyrank: setting up Kissmyrank Messages App.")
        kissmyrank["messages"]["id"] = ac.newApp("Kissmyrank Messages")
        ac.setTitle(kissmyrank["messages"]["id"], "Messages")
        ac.drawBorder(kissmyrank["messages"]["id"], 1)
        ac.setIconPosition(kissmyrank["messages"]["id"], 0, -6000)
        updateMessagesSize()
        ac.setBackgroundColor(kissmyrank["messages"]["id"], 0, 0, 0)
        ac.setBackgroundOpacity(kissmyrank["messages"]["id"], 0)
        ac.setVisible(kissmyrank["messages"]["id"], kissmyrank["messages"]["on"])
        ac.addOnAppActivatedListener(kissmyrank["messages"]["id"], onMessagesOn)
        ac.addOnAppDismissedListener(kissmyrank["messages"]["id"], onMessagesOff)
        # add text control
        for i in range(0, kissmyrank["messages"]["lines"]):
            kissmyrank["messages"]["controls"]["text_" + str(i)] = {}
            kissmyrank["messages"]["controls"]["text_" + str(i)]["id"] = ac.addLabel(kissmyrank["messages"]["id"], " ")
            ac.setCustomFont(kissmyrank["messages"]["controls"]["text_" + str(i)]["id"], kissmyrank["messages"]["font"],
                             0,
                             0)
            positionAndSizeMessage(i)
            ac.setFontColor(kissmyrank["messages"]["controls"]["text_" + str(i)]["id"], 1, 1, 1, 1)
            ac.setFontAlignment(kissmyrank["messages"]["controls"]["text_" + str(i)]["id"], "center")
            ac.setBackgroundColor(kissmyrank["messages"]["controls"]["text_" + str(i)]["id"], 0.3, 0.3, 0.3)
            ac.setBackgroundOpacity(kissmyrank["messages"]["controls"]["text_" + str(i)]["id"], 0.6)
            ac.setVisible(kissmyrank["messages"]["controls"]["text_" + str(i)]["id"], 0)
        if config["link"]["on"]:
            time.sleep(5)
            onLinkOn()
        ac.log("Kissmyrank: app initialization complete.")
        return "Kissmyrank"


    def acUpdate(deltaT):
        global applink, kissmyrank
        # update timers
        for i in range(0, len(kissmyrank["timers"])):
            kissmyrank["timers"][i] += deltaT
        # if the app was moved we set the background
        if config["UI"]["show"] == False:
            # ac.setTitle(kissmyrank["link"]["id"], "")
            # ac.drawBorder(kissmyrank["link"]["id"], 0)
            # ac.setBackgroundColor(kissmyrank["link"]["id"], 0, 0, 0)
            # ac.setBackgroundOpacity(kissmyrank["link"]["id"], 0)
            
            ac.setTitle(kissmyrank["flags"]["id"], "")
            ac.drawBorder(kissmyrank["flags"]["id"], 0)
            ac.setBackgroundColor(kissmyrank["flags"]["id"], 0, 0, 0)
            ac.setBackgroundOpacity(kissmyrank["flags"]["id"], 0)

            ac.setTitle(kissmyrank["messages"]["id"], "")
            ac.drawBorder(kissmyrank["messages"]["id"], 0)
            ac.setBackgroundColor(kissmyrank["messages"]["id"], 0, 0, 0)
            ac.setBackgroundOpacity(kissmyrank["messages"]["id"], 0)
        else:
            # ac.setTitle(kissmyrank["link"]["id"], "link")
            # ac.drawBorder(kissmyrank["link"]["id"], 1)
            # ac.setBackgroundColor(kissmyrank["link"]["id"], 0, 0, 0)
            # ac.setBackgroundOpacity(kissmyrank["link"]["id"], 0.3)

            ac.setTitle(kissmyrank["flags"]["id"], "flags")
            ac.drawBorder(kissmyrank["flags"]["id"], 1)
            ac.setBackgroundColor(kissmyrank["flags"]["id"], 0, 0, 0)
            ac.setBackgroundOpacity(kissmyrank["flags"]["id"], 0.3)

            ac.setTitle(kissmyrank["messages"]["id"], "messages")
            ac.drawBorder(kissmyrank["messages"]["id"], 1)
            ac.setBackgroundColor(kissmyrank["messages"]["id"], 0, 0, 0)
            ac.setBackgroundOpacity(kissmyrank["messages"]["id"], 0.3)


        if kissmyrank["settings"]["on"] and len(kissmyrank["settings"]["need_updating"]):
            to_update = kissmyrank["settings"]["need_updating"].pop(0)
            m = re.search("^(flags|messages)_(.+)$", to_update)
            ac.setText(kissmyrank["settings"]["controls"][to_update + "_input"]["id"],
                       str(config[m.group(1)][m.group(2)]))
        # ok let's do something
        if applink["token"]:
            if applink["sock"]:
                if kissmyrank["timers"][0] > 0.033:
                    kissmyrank["timers"][0] = 0
                    try:
                        # see if we received something
                        data, addr = applink["sock"].recvfrom(4096)
                        if data:
                            # parse it
                            r = parseData(data)
                            if r:
                                # if it's an event the result array
                                # contains the event information (first item is the id,
                                # last item is the full message localized in the user language)
                                processEvent(r)
                    except:
                        pass
                    handleEventQueue()
                    cycleActiveFlags()
                if applink["connected"] and kissmyrank["timers"][2] > 60 * (kissmyrank["fails"] + 1) \
                        and kissmyrank["fails"] < 4:
                    kissmyrank["fails"] += 1
                    ac.log("Kissmyrank Error: no connection to the server.")
                    resetAppLink()
        else:
            if not kissmyrank["started"]:
                # app just launched, let's wait 6 seconds before sending the message to the chat
                if kissmyrank["timers"][0] > 6:
                    # initialize the applink
                    KMRAppLinkInitialize()
                    kissmyrank["started"] = 1


    def processEvent(data):
        global kissmyrank
        try:
            if data[0] == "new_session":
                onNewSession()
                return
        except:
            return
        try:
            new_id = data[0]
            if len(kissmyrank["event_submap"][data[0]]):
                for arg in kissmyrank["event_submap"][data[0]]:
                    new_id += "_" + data[arg]
                if kissmyrank["event_map"][new_id]:
                    data[0] = new_id
        except:
            pass
        timers = [6]
        temp_flags = []
        temp_shows = []
        perm_flags = []
        perm_shows = []
        text_show = []
        sound = ""
        text_slot = -1
        try:
            if kissmyrank["event_map"][data[0]]:
                flags = kissmyrank["event_map"][data[0]][0]
                show = kissmyrank["event_map"][data[0]][2]
                text_show = show[len(flags):]
                for i in range(0, len(flags)):
                    try:
                        if kissmyrank["flags"]["controls"][flags[i]]["slot"] == 1:
                            temp_flags.append(flags[i])
                            temp_shows.append(show[i])
                        else:
                            perm_flags.append(flags[i])
                            perm_shows.append(show[i])
                    except:
                        pass
                sound = kissmyrank["event_map"][data[0]][1]
                text_slot = kissmyrank["event_map"][data[0]][3]
                if kissmyrank["event_map"][data[0]][4]:
                    timers = kissmyrank["event_map"][data[0]][-1:]
        except:
            pass
        if len(perm_flags):
            setFlags(perm_flags, perm_shows)
        if text_slot == -1 or len(temp_flags):
            kissmyrank["event_queue"].append([temp_flags, sound, temp_shows, text_slot, data[len(data) - 1]] + timers)
        if text_slot != -1:
            try:
                if text_show[text_slot]:
                    setMessage(data[len(data) - 1], text_slot)
                    playSound(sound)
            except:
                pass
        for i in range(0, len(text_show)):
            if not text_show[i]:
                setMessage("", i)


    def setMessage(message, slot):
        global kissmyrank
        if message:
            message = message.upper()
            ac.setText(kissmyrank["messages"]["controls"]["text_" + str(slot)]["id"], message)
            ac.setVisible(kissmyrank["messages"]["controls"]["text_" + str(slot)]["id"], 1)
        else:
            ac.setVisible(kissmyrank["messages"]["controls"]["text_" + str(slot)]["id"], 0)


    def setFlags(flags, show):
        global kissmyrank
        if len(flags):
            for i in range(0, len(flags)):
                try:
                    if kissmyrank["flags"]["controls"][flags[i]]:
                        slot = kissmyrank["flags"]["controls"][flags[i]]["slot"]
                        if show[i]:
                            try:
                                if len(kissmyrank["flags"]["active"][slot]) > 0:
                                    for f in kissmyrank["flags"]["active"][slot]:
                                        ac.setVisible(kissmyrank["flags"]["controls"][f]["id"],
                                                      0)
                                        if slot != 1:
                                            kissmyrank["flags"]["active"][slot].remove(f)
                                            kissmyrank["flags"]["active"][slot].remove(flags[i])
                            except:
                                pass
                            ac.setVisible(kissmyrank["flags"]["controls"][flags[i]]["id"], 1)
                            kissmyrank["flags"]["active"][slot].append(flags[i])
                            kissmyrank["flags"]["last_cycle"] = time.time()
                        else:
                            try:
                                kissmyrank["flags"]["active"][slot].remove(flags[i])
                                kissmyrank["flags"]["active"][slot].index(flags[i])
                            except:
                                ac.setVisible(kissmyrank["flags"]["controls"][flags[i]]["id"], 0)
                except:
                    pass


    def cycleActiveFlags():
        global kissmyrank
        now = time.time()
        try:
            if now - kissmyrank["flags"]["last_cycle"] > 1 and len(kissmyrank["flags"]["active"][1]) > 1:
                ac.setVisible(kissmyrank["flags"]["controls"][kissmyrank["flags"]["active"][1][-1]]["id"], 0)
                removed = kissmyrank["flags"]["active"][1].pop(0)
                ac.setVisible(kissmyrank["flags"]["controls"][removed]["id"], 1)
                kissmyrank["flags"]["active"][1].append(removed)
                kissmyrank["flags"]["last_cycle"] = now
        except:
            pass


    def handleEventQueue():
        global kissmyrank
        now = time.time()
        if len(kissmyrank["event_queue"]):  # 0:flags, 1:sound, 2: shows, 3:slot, 4:message, 5:max_time
            i = 0
            while i < len(kissmyrank["event_queue"]):
                try:
                    if kissmyrank["event_queue"][i][6]:
                        if now - kissmyrank["event_queue"][i][6] > kissmyrank["event_queue"][i][5]:
                            if kissmyrank["event_queue"][i][3] > 1:
                                setMessage("", kissmyrank["event_queue"][i][3])
                            setFlags(kissmyrank["event_queue"][i][0], [0] * len(kissmyrank["event_queue"][i][2]))
                            try:
                                kissmyrank["messages"]["used_slots"].remove(kissmyrank["event_queue"][i][3])
                            except:
                                pass
                            kissmyrank["event_queue"].pop(i)
                            i -= 1
                except:
                    if kissmyrank["event_queue"][i][3] == -1:
                        kissmyrank["event_queue"][i][3] = findFreeMessageSlot()
                        try:
                            kissmyrank["messages"]["used_slots"].remove(kissmyrank["event_queue"][i][3])
                        except:
                            pass
                        kissmyrank["messages"]["used_slots"].append(kissmyrank["event_queue"][i][3])
                        setMessage(kissmyrank["event_queue"][i][4], kissmyrank["event_queue"][i][3])
                        playSound(kissmyrank["event_queue"][i][1])
                    setFlags(kissmyrank["event_queue"][i][0], kissmyrank["event_queue"][i][2])
                    kissmyrank["event_queue"][i].append(now)
                i += 1


    def findFreeMessageSlot():
        global kissmyrank
        if len(kissmyrank["messages"]["used_slots"]) > 2:
            for i in range(2, 9):
                try:
                    kissmyrank["messages"]["used_slots"].index(i)
                except:
                    return i
        return 2


    def onMessage(message, by):
        global applink, kissmyrank
        if not applink["token"] and not applink["connected"] and by == "SERVER" and \
                applink["chat_fail_counter"] < 13:
            # AppLink is not initialized but there is still hope (less than 9 messages since the request)
            m = re.search("AppLink: ([^:]+):([\d]+) ([^ ]+)$", message)
            if m:
                ac.log("Kissmyrank: /kmr applink information received.")
                applink["ip"] = m.group(1)
                if not applink["ip"] or applink["ip"] == "undefined" or applink["ip"] == "auto":
                    try:
                        applink["ip"] = ac.getServerIP()
                    except:
                        pass
                applink["port"] = int(m.group(2))
                applink["token"] = m.group(3)
                if kissmyrank["link"]["on"]:
                    # the app is active let's start the stream
                    KMRAppLinkConnect()
            else:
                # too bad the message is not the right one, let's increment the fail counter
                applink["chat_fail_counter"] += 1
                if applink["chat_fail_counter"] > 12:
                    ac.log("Kissmyrank Error: there was no valid reply to the /kmr applink command.")


    def parseData(data):
        global applink, kissmyrank
        result = []
        if ord(data[0:1].decode("iso-8859-1")) == 1:
            # keepalive (currently only contains the Kissmyrank position)
            applink["position"] = ord(data[1:2].decode("iso-8859-1"))
            if not applink["connected"]:
                ac.log("Kissmyrank: the AppLink connection has been successfully established. Ready for events.")
                applink["connected"] = 1
            kissmyrank["fails"] = 0
            kissmyrank["timers"][2] = 0
            if kissmyrank["heartbeat"] % 3 == 0:
                kissmyrank["heartbeat"] = 0
                try:
                    applink["sock"].sendto(chr(0).encode("iso-8859-1"), (applink["ip"], applink["port"]))
                except:
                    pass
            kissmyrank["heartbeat"] += 1
            return None
        else:
            # if we're here, it's an event
            start = 1
            while start < len(data):
                # let's parse it
                try:
                    length = ord(data[start:start + 1].decode("iso-8859-1")) * 4
                    temp = data[start + 1:start + 1 + length]
                    result.append(temp.decode("utf-32le"))
                    start += 1 + length
                except:
                    return result
            return result


    def onNewSession():
        global kissmyrank
        for i in range(0, 3):
            for flag in kissmyrank["flags"]["active"][i]:
                setFlags([flag], [0])
        for i in range(0, len(kissmyrank["messages"]["controls"])):
            setMessage("", i)


    # noinspection PyUnusedLocal
    def onLinkOn(*args):
        global kissmyrank, applink
        kissmyrank["link"]["on"] = 1
        if applink["token"]:
            # the AppLink was already initialized
            if not applink["connected"]:
                # but we're not connected, let's start the stream
                KMRAppLinkConnect()
        else:
            # the AppLink was not initialized, let's intialize it
            KMRAppLinkInitialize()
        if config["link"]["on"] != 1:
            config["link"]["on"] = 1
            configSave()
        try:
            ac.addOnChatMessageListener(kissmyrank["messages"]["id"], onMessage)
        except:
            pass
        try:
            ac.addOnChatMessageListener(kissmyrank["flags"]["id"], onMessage)
        except:
            pass



    # noinspection PyUnusedLocal
    def onLinkOff(*args):
        global kissmyrank
        kissmyrank["link"]["on"] = 0
        # let's stop the stream
        KMRAppLinkDisconnect()
        if config["link"]["on"] != 0:
            config["link"]["on"] = 0
            configSave()


    # noinspection PyUnusedLocal
    def onFlagsOn(*args):
        global kissmyrank
        kissmyrank["flags"]["on"] = 1
        ac.setVisible(kissmyrank["flags"]["id"], kissmyrank["flags"]["on"])
        if config["flags"]["on"] != 1:
            config["flags"]["on"] = 1
            configSave()
        # onLinkOn(*args)


    # noinspection PyUnusedLocal
    def onFlagsOff(*args):
        global kissmyrank
        kissmyrank["flags"]["on"] = 0
        ac.setVisible(kissmyrank["flags"]["id"], kissmyrank["flags"]["on"])
        if config["flags"]["on"] != 0:
            config["flags"]["on"] = 0
            configSave()
        # if config["messages"]["on"] == 0 and config["flags"]["on"] == 0:
        #     onLinkOff(*args)


    # noinspection PyUnusedLocal
    def onMessagesOn(*args):
        global kissmyrank
        kissmyrank["messages"]["on"] = 1
        ac.setVisible(kissmyrank["messages"]["id"], kissmyrank["messages"]["on"])
        if config["messages"]["on"] != 1:
            config["messages"]["on"] = 1
            configSave()
        # onLinkOn(*args)


    # noinspection PyUnusedLocal
    def onMessagesOff(*args):
        global kissmyrank
        kissmyrank["messages"]["on"] = 0
        ac.setVisible(kissmyrank["messages"]["id"], kissmyrank["messages"]["on"])
        if config["messages"]["on"] != 0:
            config["messages"]["on"] = 0
            configSave()
        # if config["messages"]["on"] == 0 and config["flags"]["on"] == 0:
        #     onLinkOff(*args)


    # noinspection PyUnusedLocal
    def onSettingsOn(*args):
        global kissmyrank
        kissmyrank["settings"]["on"] = 1
        ac.setVisible(kissmyrank["settings"]["id"], kissmyrank["settings"]["on"])


    # noinspection PyUnusedLocal
    def onSettingsOff(*args):
        global kissmyrank
        kissmyrank["settings"]["on"] = 0
        ac.setVisible(kissmyrank["settings"]["id"], kissmyrank["settings"]["on"])


    def KMRAppLinkConnect():
        KMRAppLinkSetStatus(1)


    def KMRAppLinkDisconnect():
        KMRAppLinkSetStatus(0)


    def KMRAppLinkSetStatus(new_status):
        global applink
        if applink["connected"] != new_status and applink["ip"] and applink["port"] and \
                applink["token"] and len(applink["token"]) == 6:
            # we have everything we need
            if not applink["sock"]:
                ac.log("Kissmyrank: binding socket.")
                try:
                    applink["sock"] = socket.socket(socket.AF_INET,  # Internet
                                                    socket.SOCK_DGRAM)  # UDP
                    # we don't want to freeze AC
                    applink["sock"].settimeout(0.001)
                    applink["sock"].bind(("".encode("ascii"), 0))
                except:
                    ac.log("Kissmyrank Error:" + str(traceback.format_exc()))
                    ac.log("Kissmyrank Error: cannot bind socket. Trying different settings (1).")
                    try:
                        applink["sock"].bind(("0.0.0.0".encode("ascii"), 11235))
                    except:
                        ac.log("Kissmyrank Error:" + str(traceback.format_exc()))
                        ac.log("Kissmyrank Error: cannot bind socket. Trying different settings (2).")
                        try:
                            u'wtf'.encode('idna')
                        except:
                            pass
                        try:
                            applink["sock"].bind(("", 0))
                        except:
                            ac.log("Kissmyrank Error:" + str(traceback.format_exc()))
                            ac.log("Kissmyrank Error: cannot bind socket. Trying different settings (3).")
                            try:
                                applink["sock"].bind((u"".encode('idna'), 0))
                            except:
                                ac.log("Kissmyrank Error:" + str(traceback.format_exc()))
                                ac.log("Kissmyrank Error: cannot bind socket. Please check your firewall.")
            # let's create the request
            request = chr(len(applink["app_id"])).encode("iso-8859-1") + applink["app_id"].encode('utf-32le') + \
                      chr(len(applink["token"])).encode("iso-8859-1") + applink["token"].encode('utf-32le') + \
                      chr(new_status).encode("iso-8859-1")
            ac.log("Kissmyrank: attempting to establish the AppLink connection.")
            try:
                applink["sock"].sendto(request, (applink["ip"], applink["port"]))
            except:
                ac.log("Kissmyrank Error: cannot send the request.")
                return
            if not new_status:
                # if we are stopping the stream let's update the status
                applink["connected"] = new_status


    def KMRAppLinkInitialize():
        global applink
        # let's reset the fail counter
        applink["chat_fail_counter"] = 0
        ac.log("Kissmyrank: sending the /kmr applink command.")
        ac.sendChatMessage("/kmr applink")


    def configSave():
        global config
        try:
            with open(config["config_file_path"], 'w') as config_file:
                config_file.write(json.dumps(config))
            ac.log("Kissmyrank: config saved.")
        except:
            pass


    def settingsNextLine(padding=24):
        global kissmyrank
        kissmyrank["settings"]["cursor"] += padding


    def addSettingsTextInput(control_id, text, handler):
        global kissmyrank, config
        m = re.search("^(flags|messages)_(.+)$", control_id)
        control_id += "_input"
        kissmyrank["settings"]["controls"][control_id + "_label"] = {}
        kissmyrank["settings"]["controls"][control_id + "_label"]["id"] = ac.addLabel(kissmyrank["settings"]["id"],
                                                                                      text)
        ac.setPosition(kissmyrank["settings"]["controls"][control_id + "_label"]["id"], 3,
                       kissmyrank["settings"]["cursor"])
        settingsNextLine()
        kissmyrank["settings"]["controls"][control_id] = {}
        kissmyrank["settings"]["controls"][control_id]["id"] = ac.addTextInput(kissmyrank["settings"]["id"],
                                                                               "Flags Width:")
        ac.setPosition(kissmyrank["settings"]["controls"][control_id]["id"], 3,
                       kissmyrank["settings"]["cursor"])
        ac.setSize(kissmyrank["settings"]["controls"][control_id]["id"],
                   kissmyrank["settings"]["width"] - 6,
                   24)

        ac.setText(kissmyrank["settings"]["controls"][control_id]["id"], str(config[m.group(1)][m.group(2)]))
        ac.addOnValidateListener(kissmyrank["settings"]["controls"][control_id]["id"], handler)
    
    def addSettingsBoxInput(control_id, text, handler):
        global kissmyrank, config
        m = re.search("^(flags|messages)_(.+)$", control_id)
        control_id += "_input"
        kissmyrank["settings"]["controls"][control_id + "_label"] = {}
        kissmyrank["settings"]["controls"][control_id + "_label"]["id"] = ac.addLabel(kissmyrank["settings"]["id"],
                                                                                      text)
        ac.setPosition(kissmyrank["settings"]["controls"][control_id + "_label"]["id"], 3,
                       kissmyrank["settings"]["cursor"])
        settingsNextLine()
        kissmyrank["settings"]["controls"][control_id] = {}
        kissmyrank["settings"]["controls"][control_id]["id"] = ac.addButton(kissmyrank["settings"]["id"],
                                                                               "Yes" if config["UI"]["show"] else "No")
        ac.setPosition(kissmyrank["settings"]["controls"][control_id]["id"], 3,
                       kissmyrank["settings"]["cursor"])
        ac.setSize(kissmyrank["settings"]["controls"][control_id]["id"],
                   kissmyrank["settings"]["width"] - 6,
                   24)
        ac.addOnClickedListener(kissmyrank["settings"]["controls"][control_id]["id"], handler)


    def onFlagsWidthChange(*args):
        global config, kissmyrank
        config["flags"]["width"] = int(args[0])
        ac.setText(kissmyrank["settings"]["controls"]["flags_width_input"]["id"], str(config["flags"]["width"]))
        configSave()
        positionFlags()
        updateFlagsSize()
        kissmyrank["settings"]["need_updating"].append("flags_width")


    def onFlagsHeightChange(*args):
        global config, kissmyrank
        config["flags"]["height"] = int(args[0])
        ac.setText(kissmyrank["settings"]["controls"]["flags_height_input"]["id"], str(config["flags"]["height"]))
        configSave()
        positionFlags()
        updateFlagsSize()
        kissmyrank["settings"]["need_updating"].append("flags_height")


    def onFlagsSpacingChange(*args):
        global config, kissmyrank
        config["flags"]["spacing"] = int(args[0])
        ac.setText(kissmyrank["settings"]["controls"]["flags_spacing_input"]["id"], str(config["flags"]["spacing"]))
        configSave()
        positionFlags()
        updateFlagsSize()
        kissmyrank["settings"]["need_updating"].append("flags_spacing")


    def positionFlags():
        global kissmyrank
        for id_, flag in kissmyrank["flags"]["controls"].items():
            positionFlag(id_)


    def positionFlag(id_):
        global kissmyrank, config
        try:
            if config["flags"]["layout"] == "horizontal":
                flag_width = (config["flags"]["width"] - 2 * config["flags"]["spacing"]) / 3
                ac.setPosition(kissmyrank["flags"]["controls"][id_]["id"],
                               kissmyrank["flags"]["controls"][id_]["slot"] * (flag_width + config["flags"]["spacing"]),
                               0)
                ac.setSize(kissmyrank["flags"]["controls"][id_]["id"], flag_width,
                           config["flags"]["height"])
            else:
                flag_height = (config["flags"]["height"] - 2 * config["flags"]["spacing"]) / 3
                ac.setPosition(kissmyrank["flags"]["controls"][id_]["id"],
                               0, kissmyrank["flags"]["controls"][id_]["slot"] * (
                                       flag_height + config["flags"]["spacing"]))
                ac.setSize(kissmyrank["flags"]["controls"][id_]["id"], config["flags"]["width"],
                           flag_height)
        except:
            ac.log("Kissmyrank Error:" + str(traceback.format_exc()))


    def onMessagesWidthChange(*args):
        global config, kissmyrank
        config["messages"]["width"] = int(args[0])
        ac.setText(kissmyrank["settings"]["controls"]["messages_width_input"]["id"], str(config["messages"]["width"]))
        configSave()
        positionAndSizeMessages()
        updateMessagesSize()
        kissmyrank["settings"]["need_updating"].append("messages_width")


    def onMessagesFontSizeChange(*args):
        global config, kissmyrank
        config["messages"]["font_size"] = int(args[0])
        ac.setText(kissmyrank["settings"]["controls"]["messages_font_size_input"]["id"],
                   str(config["messages"]["font_size"]))
        configSave()
        positionAndSizeMessages()
        updateMessagesSize()
        kissmyrank["settings"]["need_updating"].append("messages_font_size")


    def onMessagesLineHeightChange(*args):
        global config, kissmyrank
        config["messages"]["line_height"] = int(args[0])
        ac.setText(kissmyrank["settings"]["controls"]["messages_line_height_input"]["id"],
                   str(config["messages"]["line_height"]))
        configSave()
        positionAndSizeMessages()
        updateMessagesSize()
        kissmyrank["settings"]["need_updating"].append("messages_line_height")


    def onMessagesSpacingChange(*args):
        global config, kissmyrank
        config["messages"]["spacing"] = int(args[0])
        ac.setText(kissmyrank["settings"]["controls"]["messages_spacing_input"]["id"],
                   str(config["messages"]["spacing"]))
        configSave()
        positionAndSizeMessages()
        updateMessagesSize()
        kissmyrank["settings"]["need_updating"].append("messages_spacing")

    def onUISettingChange(*args):
        global config, kissmyrank
        current = config["UI"]["show"]
        new = not current
        config["UI"]["show"] = new
        ac.setText(kissmyrank["settings"]["controls"]["messages_ui_input"]["id"], "Yes" if config["UI"]["show"] else "No")
        configSave()
        kissmyrank["settings"]["need_updating"].append("messages_ui")
    
    def onKMRConnectChange(*args):
        global config, kissmyrank
        current = config["link"]["on"]
        new = not current
        config["link"]["on"] = new
        if config["link"]["on"]:
            onLinkOn(*args)
        else:
            onLinkOff(*args)
        ac.setText(kissmyrank["settings"]["controls"]["connect_KMR_input"]["id"], "Yes" if config["link"]["on"] else "No")
        configSave()
        kissmyrank["settings"]["need_updating"].append("messages_connect")


    def positionAndSizeMessages():
        global kissmyrank
        for i in range(0, kissmyrank["messages"]["lines"]):
            positionAndSizeMessage(i)


    def positionAndSizeMessage(i):
        global kissmyrank, config
        try:
            ac.setPosition(kissmyrank["messages"]["controls"]["text_" + str(i)]["id"], 0,
                           (config["messages"]["line_height"] + config["messages"]["spacing"]) * i)
            ac.setSize(kissmyrank["messages"]["controls"]["text_" + str(i)]["id"], config["messages"]["width"],
                       config["messages"]["line_height"])
            ac.setFontSize(kissmyrank["messages"]["controls"]["text_" + str(i)]["id"],
                           config["messages"]["font_size"])
        except:
            ac.log("Kissmyrank Error:" + str(traceback.format_exc()))


    def flagsLayoutHighlight(flag_layout):
        global kissmyrank, config
        if flag_layout == config["flags"]["layout"]:
            ac.setBackgroundColor(kissmyrank["settings"]["controls"]["flags_layouts"][flag_layout]["id"], 0, 0.3, 0)
            ac.setBackgroundOpacity(kissmyrank["settings"]["controls"]["flags_layouts"][flag_layout]["id"], 1)
        else:
            ac.setBackgroundColor(kissmyrank["settings"]["controls"]["flags_layouts"][flag_layout]["id"], 0, 0.0, 0)
            ac.setBackgroundOpacity(kissmyrank["settings"]["controls"]["flags_layouts"][flag_layout]["id"], 0.6)


    def flagsLayoutHighlightUpdate():
        flag_layouts = ["horizontal", "vertical"]
        for flag_layout in flag_layouts:
            flagsLayoutHighlight(flag_layout)


    def imagePackHighlight(image_pack):
        global kissmyrank, config
        if image_pack == config["image_pack"]:
            ac.setBackgroundColor(kissmyrank["settings"]["controls"]["image_packs"][image_pack]["id"], 0, 0.3, 0)
            ac.setBackgroundOpacity(kissmyrank["settings"]["controls"]["image_packs"][image_pack]["id"], 1)
        else:
            ac.setBackgroundColor(kissmyrank["settings"]["controls"]["image_packs"][image_pack]["id"], 0, 0, 0)
            ac.setBackgroundOpacity(kissmyrank["settings"]["controls"]["image_packs"][image_pack]["id"], 0.6)


    def imagePackHighlightUpdate():
        global kissmyrank
        image_packs = kissmyrank["image_packs"]
        for image_pack in image_packs:
            imagePackHighlight(image_pack)


    def soundPackHighlight(sound_pack):
        global kissmyrank, config
        if sound_pack == config["sound_pack"]:
            ac.setBackgroundColor(kissmyrank["settings"]["controls"]["sound_packs"][sound_pack]["id"], 0, 0.3, 0)
            ac.setBackgroundOpacity(kissmyrank["settings"]["controls"]["sound_packs"][sound_pack]["id"], 1)
        else:
            ac.setBackgroundColor(kissmyrank["settings"]["controls"]["sound_packs"][sound_pack]["id"], 0, 0, 0)
            ac.setBackgroundOpacity(kissmyrank["settings"]["controls"]["sound_packs"][sound_pack]["id"], 0.6)


    def soundPackHighlightUpdate():
        global kissmyrank
        sound_packs = kissmyrank["sound_packs"]
        for sound_pack in sound_packs:
            soundPackHighlight(sound_pack)


    def updateFlagsSize():
        global config, kissmyrank
        ac.setSize(kissmyrank["flags"]["id"], config["flags"]["width"], config["flags"]["height"])
        ac.setBackgroundOpacity(kissmyrank["flags"]["id"], 1)


    def updateMessagesSize():
        global config, kissmyrank
        ac.setSize(kissmyrank["messages"]["id"], config["messages"]["width"],
                   (config["messages"]["line_height"] + config["messages"]["spacing"]) * kissmyrank["messages"][
                       "lines"])
        ac.setBackgroundOpacity(kissmyrank["messages"]["id"], 1)


    def playSound(sound):
        global config
        if config["sound_pack"] != "mute" and sound:
            try:
                winsound.PlaySound(os.path.join(config["sound_base_path"], config["sound_pack"], sound),
                                   winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_NODEFAULT)
            except:
                ac.log("Kissmyrank Error: cannot play sound.")


    def resetAppLink():
        global applink, kissmyrank
        ac.log("Kissmyrank: resetting the applink.")
        kissmyrank["timers"][2] = 0
        applink["connected"] = 0
        applink["token"] = 0
        applink["ip"] = ""
        applink["port"] = 0
        applink["chat_fail_counter"] = 99
        applink["position"] = 0
        kissmyrank["timers"][0] = 0
        kissmyrank["started"] = 0


except:
    ac.log("Kissmyrank Error:" + str(traceback.format_exc()))
