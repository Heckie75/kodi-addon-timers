# kodi-addon-timers
Powerful timers for KODI

I wanted to have a KODI addon that is a sleep timer, a doze timer, has several other timer slots and combines it with fading volume in and out over a certain period. Since I haven't found it I decided to program it by myself.

The result is a powerful timer addon.

## Overview of features:
* Unlimited timer slots. All of them can be quickly set up by using context menu
* single-click-setup for sleep and doze timers
* Timers can play any resource that it available in KODI, e.g. music folders, video files, TV/radio programs, slideshows, resources from 3rd party plugins, e.g. Zattoo channels.
* Timers can be set from TV / Radio EPG, One-click-setup from epg (Quick Timer)
* Different schedule modes: once, everyday, Mon-Fri, Fri-Sat, Sat-Sun, Sun-Thu, Mon-Thu, specific weekday and many more
* Date change is supported, e.g. from 23:30 (p.m.) until 1:30 (a.m.)
* Shuffle, repeat, 2 end modes, i.e. duration or specific time
* Actions related to media: start media and stop at end, just start media, start media at end, stop media immediately, stop media at end, power down system
* Linear fading in timer period: fade-in, fade-out, no fading. Min and max volume can be set for each timer
* Custom label for timer
* After KODI startup timers, that are in period, start retroactively although KODI was not running at start time. Fading volume is calculated correctly.
* Feature in order to prevent that display is turned off if KODI idles but is not in full screen mode
* MS Windows only: Feature in order to prevent that Windows displays lock screen if KODI idles

<img src="script.timers/resources/assets/screenshot_01.png?raw=true">

<img src="script.timers/resources/assets/screenshot_02.png?raw=true">

<img src="script.timers/resources/assets/screenshot_03.png?raw=true">

<img src="script.timers/resources/assets/screenshot_04.png?raw=true">

<img src="script.timers/resources/assets/screenshot_05.png?raw=true">

<img src="script.timers/resources/assets/screenshot_06.png?raw=true">

<img src="script.timers/resources/assets/screenshot_07.png?raw=true">

<img src="script.timers/resources/assets/screenshot_08.png?raw=true">

<img src="script.timers/resources/assets/screenshot_09.png?raw=true">

## Changelog
v3.5.0 (2023-02-07)
- New feature: priority of timers and competitive behavior
- New feature: System action to put playing device on standby via a CEC peripheral
- Fixed issue so that favorites can be scheduled again

v3.4.0 (2023-01-10)
- New feature: Media action in order to pause audio or video, feature request #21
- Refactoring: moved state to timer object
- Reorganized setting levels (simple, standard, advanced, expert)
- Introduced logging (see kodi.log)

v3.3.2 (2022-12-01)
- Improved logging

v3.3.1 (2022-11-26)
- Bugfix: scheduled timers stop working that are scheduled after Sunday (week change Sun -> Mon)
- Refactoring

v3.3.0 (2022-10-08)
- Added fields for start and end time in order to schedule to the second (expert only)
- Improved scheduler that enables scheduling to the second, reduces CPU load and enables smoother fading
- Fixed Zattoo PVR support and other audio/video addons

v3.2.0 (2022-08-27)
- Unlimited amount of timers
- Added feature in order to pause timers for a certain period
- Set adequate label for playing items instead of internal path
- Added global configurable offset in order to perform timers ahead of time or later in time
- Changed context menu 'timers' for EPG
- Changed resume behavior if there are two parallel ending timers so that non-resuming timer wins and stops media
- Added dialog in order to abort system action
- Added help texts for all settings

v3.1.0 (2022-05-26)
- Added feature in order to schedule slideshows, program/script addons and favorites
- Free selection of weekdays
- Added feature for shuffling playlists
- Improved resuming, e.g. in case of media that is shorter than timer
- optimization and bugfixes, e.g. preview of playlists / folders
- covered and proved many timer scenarios and functionality with unit tests

v3.0.0 (2022-04-12)
- Support folders and playlists for scheduling, (feature request https://github.com/Heckie75/kodi-addon-timers/issues/7)
- Separated configuration of media and system actions, e.g. shutdown KODI
- Enable resuming media that has been stopped after timer has finished
- Enable repeating media and playlists
- Refactoring (rewrite of scheduler)

v2.1.2 (2022-02-09)
- Device wakeup (Issue #6): Explicitly activate CEC Source before player starts

v2.1.1 (2022-01-29)
- Improved behavior after update addon. No need to restart KODI anymore after update
- Improved prevention lock screen, no restart of KODI required anymore after setting has changed
- Refactoring: Usage of modern KODI API (read and write settings)
- Added timer actions, i.e. quit KODI, suspend system, hibernate system, shutdown system
- Minor bugfixes, e.g. displayed wrong timer no. in some dialogs

v2.1.0 (2021-11-20):
- Improved start and stop action in case that multiple timers are running in parallel, see also https://github.com/Heckie75/kodi-addon-timers/issues/5
- One-click-setup from epg (Quick Timer)
- Improved procedure of update state after one-time-timers have run out or settings have been changed
- Added 5 more timer slots
- Added feature in order to prevent that display is turned off if KODI idles but is not in full screen mode
- Migrated to new XML settings format
- Major refactoring, better structured code

v2.0.3 (2021-10-31)
- Fixed issue related to reset to default settings after one-time timers has finished
- Fixed issue that wrong pvr channel was taken from epg if some channels are deactivated in PVR
- Fixed key error after deactivating timer

v2.0.2 (2021-10-03)
- Improvement: prevent multiple fading action of overlapping fading timers. Strategy is 'First starts first served.'
- reset to default settings after one-time timers finished
- minor refactoring

v2.0.1 (2021-09-12)
- Bugfix: actions in settings dialog don't work, i.e. 'reset volume' and 'play now'

v2.0.0 (2021-07-18)
- Migration to KODI 19 (Matrix)
- Total refactoring of earlier version