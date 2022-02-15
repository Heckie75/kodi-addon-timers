# kodi-addon-timers
Powerful timers for KODI

I wanted to have a Kodi addon that is a sleep timer, a doze timer, has several other timer slots and combines it with fading volume in and out over a certain period. Since I haven't found it I decided to program it by myself. 

The result is a powerful timer addon.  

## Overview of features:
* 15 timer slots. All of them can be quickly set up by using context menu
* 2 additional slots for sleep and doze timers with single-click-setup 
* Timers can play any ressource that it available in Kodi, e.g. music, video files, TV/radio programs, ressources from 3rd party plugins, e.g. Zattoo channels. 
* Timers can be set from TV / Radio EPG
* Different schedule modes: once, everyday, Mon-Fri, Fri-Sat, Sat-Sun, Sun-Thu, Mon-Thu, specific weekday and many more
* Date change is supported, e.g. from 23:30 (p.m.) until 1:30 (a.m.) 
* Two end modes, i.e. duration or specific time
* Actions related to media: start media and stop at end, just start media, start media at end, stop media immediately, stop media at end, powerdown system
* Linear fading in timer period: fade-in, fade-out, no fading. Min and max volume can be set for each timer
* Custom label for timer
* After KODI startup timers, that are in period, start retroactivly altought KODI was not running at start time. Fading volume is calculated correctly.
* MS Windows only: Feature in order to prevent that Windows displays lock screen if Kodi idles

<img src="script.timers/resources/assets/screenshot_01.png?raw=true">

<img src="script.timers/resources/assets/screenshot_02.png?raw=true">

<img src="script.timers/resources/assets/screenshot_03.png?raw=true">

<img src="script.timers/resources/assets/screenshot_04.png?raw=true">

<img src="script.timers/resources/assets/screenshot_05.png?raw=true">

<img src="script.timers/resources/assets/screenshot_06.png?raw=true">

<img src="script.timers/resources/assets/screenshot_07.png?raw=true">

<img src="script.timers/resources/assets/screenshot_08.png?raw=true">

<img src="script.timers/resources/assets/screenshot_09.png?raw=true">

<img src="script.timers/resources/assets/screenshot_10.png?raw=true">

## Changelog
v2.1.2 (2022-02-09)
- Device wakeup (Issue #6): Explicitly activate CEC Source before player starts

v2.1.1 (2022-01-29)
- Improved behaviour after update addon. No need to restart Kodi anymore after update
- Improved prevention lock screen, no restart of Kodi required anymore after setting has changed
- Refactoring: Usage of modern Kodi API (read and write settings)
- Added timer actions, i.e. quit Kodi, suspend system, hibernate system, shutdown system
- Minor bugfixes, e.g. displayed wrong timer no. in some dialogs 

v2.1.0 (2021-11-20):
- Improved start and stop action in case that multiple timers are running in parallel, see also https://github.com/Heckie75/kodi-addon-timers/issues/5 
- One-click-setup from epg (Quick Timer)
- Improved procedure of update state after one-time-timers have run out or settings have been changed
- Added 5 more timer slots
- Added feature in order to prevent that display is turned off if Kodi idles but is not in fullscreen mode
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
- Migration to Kodi 19 (Matrix)
- Total refactoring of earlier version