# kodi-addon-timers
Powerful timers for KODI

I wanted to have a Kodi addon that is a sleep timer, a doze timer, has several other timer slots and combines it with fading volume in and out over a certain period. Since I haven't found it I decided to program it by myself.

The result is a powerful timer addon.

## Overview of features:
* Unlimited timer slots. All of them can be quickly set up by using context menu
* single-click-setup for sleep and doze timers
* Timers can play any resource that it available in Kodi, e.g. music folders, video files, TV/radio programs, slideshows, ressources from 3rd party plugins, e.g. Zattoo channels.
* Timers can be set from TV / Radio EPG, One-click-setup from epg (Quick Timer)
* Different schedule modes: once, everyday, Mon-Fri, Fri-Sat, Sat-Sun, Sun-Thu, Mon-Thu, specific weekday and many more
* Date change is supported, e.g. from 23:30 (p.m.) until 1:30 (a.m.)
* Shuffle, repeat, 2 end modes, i.e. duration or specific time
* Actions related to media: start media and stop at end, just start media, start media at end, stop media immediately, stop media at end, powerdown system
* Linear fading in timer period: fade-in, fade-out, no fading. Min and max volume can be set for each timer
* Custom label for timer
* After KODI startup timers, that are in period, start retroactivly although KODI was not running at start time. Fading volume is calculated correctly.
* Feature in order to prevent that display is turned off if Kodi idles but is not in fullscreen mode
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

## Changelog
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
- Changed resume behaviour if there are two parallel ending timers so that non-resuming timer wins and stops media
- Added dialog in order to abort system action
- Added help texts for all settings

v3.1.0 (2022-05-26)
- Added feature in order to schedule slideshows, program/script addons and favourites
- Free selection of weekdays
- Added feature for shuffling playlists
- Improved resuming, e.g. in case of media that is shorter than timer
- optimization and bugfixes, e.g. preview of playlists / folders
- covered and proved many timer scenarios and functionality with unit tests

v3.0.0 (2022-04-12)
- Support folders and playlists for scheduling, (feature request https://github.com/Heckie75/kodi-addon-timers/issues/7)
- Separated configuration of media and system actions, e.g. shutdown Kodi
- Enable resuming media that has been stopped after timer has finished
- Enable repeating media and playlists
- Refactoring (rewrite of scheduler)

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


## Overview of supported timer scenarios
### TC 1. Single timer
#### TC 1.1. Single timer w/ resume but w/o former media
```
Timer 1           |----+---+---+----R                       (tested w/ PVR and Playlist)

t       |---------|-------T1--------|---------------->
        t0        t1       t2       t3       t4
Player            play              stop
```

Tested:
- [x] v2.2.0 pre19
- [x] v2.2.0 pre20
- [x] v2.2.0 pre21

<sup>Note: Tested with PVR (no seeking possible) and playlists and non-weekly timer</sup>

#### TC 1.2. Single timer w/ resume and w/ former media

```
Media 1 |---+---+-|                 |----+---+---+---->     (tested w/ PVR and Playlist)
Timer 1           |-----+----+------R

t       |----M1---|-------T1--------|--------M1------->     (tested w/ PVR and Playlist)
        t0        t1       t2       t3       t4
Player            play              resume
```

Tested:
- [x] v2.2.0 pre19
- [x] v2.2.0 pre20
- [x] v2.2.0 pre21

<sup>Note: Tested with PVR (no seeking possible) and playlists and non-weekly timer</sup>

#### TC 1.3. Single timer w/o resume and w/ former media

```
Media 1 |---------|                                         (tested w/ PVR and Playlist)
Timer 1           |-----------------X                       (tested w/ PVR and Playlist)

t       |----M1---|-------T1--------|---------------->
        t0        t1       t2       t3       t4
Player            play              stop
```

Tested:
- [x] v2.2.0 pre20
- [x] v2.2.0 pre21

<sup>Note: Tested with PVR (no seeking possible) and playlists and non-weekly timer</sup>

### TC 2. Overlapping timers
#### TC 2.1. Overlapping timers w/ resume but w/o former media
```
Timer 1           |------------------R
Timer 2                      |-----------------R

t       |---------|----T1----|-------T2--------|----->
        t0        t1    t2   t3  t4  t5   t6   t7   t8
Player            play       play              stop
```

Tested:
- [x] v2.2.0 pre19
- [x] v2.2.0 pre20
- [x] v2.2.0 pre21

<sup>Note: Tested with PVR (no seeking possible) and playlists and non-weekly timer</sup>

#### TC 2.2. Overlapping timers w/ resume and w/ former media
```
Media 1 |---------|                            |---------------->
Timer 1           |------------------R
Timer 2                      |-----------------R

t       |----M1---|----T1----|-------T2--------|-------M1-------->
        t0        t1    t2   t3  t4  t5   t6   t7   t8
Player            play       play              resume
```

Tested:
- [x] v2.2.0 pre19
- [x] v2.2.0 pre20
- [x] v2.2.0 pre21

<sup>Note: Tested with PVR (no seeking possible) and non-weekly timer</sup>

#### TC 2.3.  Overlapping timers w/o resume and w/ former media

##### TC 2.3.1. T1 and T2 are no resumers
```
Media 1 |---------|
Timer 1           |------------------X
Timer 2                      |-----------------X

t       |----M1---|----T1----|-------T2--------|---------------->
        t0        t1    t2   t3  t4  t5   t6   t7   t8
Player            play       play              stop
```

Tested:
- [x] v2.2.0 pre20
- [x] v2.2.0 pre21

<sup>Note: Tested with PVR (no seeking possible) and non-weekly timer</sup>

##### TC 2.3.2. Only T1 is no resumer
```
Media 1 |---------|
Timer 1           |------------------X
Timer 2                      |-----------------R

t       |----M1---|----T1----|-------T2--------|---------------->
        t0        t1    t2   t3  t4  t5   t6   t7   t8

Player            play       play              stop
```

Tested:
- [x] v2.2.0 pre20
- [ ] v2.2.0 pre21 - T2 resumes T1
- [x] v2.2.0 pre22 - Unit tests OK, manual test OK

<sup>Note: Tested with PVR (no seeking possible) and non-weekly timer</sup>

##### TC 2.3.3. Only T2 is no resumer
```
Media 1 |---------|
Timer 1           |------------------R
Timer 2                      |-----------------X

t       |----M1---|----T1----|-------T2--------|---------------->
        t0        t1    t2   t3  t4  t5   t6   t7   t8
Player            play       play              stop
```

Tested:
- [x] v2.2.0 pre20
- [x] v2.2.0 pre21

<sup>Note: Tested with PVR (no seeking possible) and non-weekly timer</sup>

## TC 3. Chained timers
#### TC 3.1. Chained timers w/ resume but w/o former media
```
Timer 1           |----------R
Timer 2                      |-----------------R

t       |---------|----T1----|-------T2--------|--------->
        t0        t1   t2    t3      t4        t5      t6
Player            play       play              stop
```

Tested:
- [x] v2.2.0 pre19
- [x] v2.2.0 pre20
- [x] v2.2.0 pre21

<sup>Note: Tested with PVR (no seeking possible) and non-weekly timer</sup>

#### TC 3.2. Chained timers w/ resume and w/ former media
```
Media 1 |---------|                            |---------------->
Timer 1           |----------R
Timer 2                      |-----------------R

t       |----M1---|----T1----|-------T2--------|-------M1-------->
        t0        t1   t2    t3      t4        t5      t6
Player            play       play              resume
```

Tested:
- [x] v2.2.0 pre19
- [x] v2.2.0 pre20
- [x] v2.2.0 pre21

<sup>Note: Tested with PVR (no seeking possible) and non-weekly timer</sup>


#### TC 3.3. Chained timers timers w/o resume and w/ former media
##### TC 3.3.1. T1 and T2 are no resumers
```
Media 1 |---------|
Timer 1           |----------X
Timer 2                      |-----------------X

t       |----M1---|----T1----|-------T2--------|--------------->
        t0        t1   t2    t3      t4        t5      t6
Player            play       play              stop
```

Tested:
- [x] v2.2.0 pre20
- [x] v2.2.0 pre21

<sup>Note: Tested with PVR (no seeking possible) and non-weekly timer</sup>

##### TC 3.3.2. Only T1 is no resumer
```
Media 1 |---------|
Timer 1           |----------X
Timer 2                      |-----------------R

t       |----M1---|----T1----|-------T2--------|--------------->
        t0        t1   t2    t3      t4        t5      t6
Player            play       play              stop
```

Tested:
- [x] v2.2.0 pre20
- [ ] v2.2.0 pre21 - ident. 2.3.2: T2 resumes T1
- [x] v2.2.0 pre22 - Unit tests OK, manual test OK

<sup>Note: Tested with PVR (no seeking possible) and non-weekly timer</sup>

##### TC 3.3.3. Only T2 is no resumer
```
Media 1 |---------|
Timer 1           |----------R
Timer 2                      |-----------------X
        t0        t1   t2    t3      t4        t5      t6
t       |----M1---|----T1----|-------T2--------|--------------->
Player            play       play              stop
```

Tested:
- [x] v2.2.0 pre20
- [x] v2.2.0 pre21

<sup>Note: Tested with PVR (no seeking possible) and non-weekly timer</sup>

## TC 4. Nested timers
### TC 4.1. Nested timer w/ resume but w/o former media
```
Timer 1           |-------------------------R
Timer 2                  |------R

t       |---------|--T1--|--T2--|---T1------|---------->
        t0        t1 t2  t3 t4  t5   t6     t7   t8
Player            play   play   resume
```

Tested:
- [x] v2.2.0 pre19
- [x] v2.2.0 pre20
- [x] v2.2.0 pre21

<sup>Note: Tested with PVR (no seeking possible) and non-weekly timer</sup>

### TC 4.2. Nested timer w/ resume and w/ former media
```
Media 1 |---------|                         |---------------->
Timer 1           |-------------------------R
Timer 2                  |------R

t       |----M1---|--T1--|--T2--|---T1------|------M1-------->
        t0        t1 t2  t3 t4  t5   t6     t7   t8
Player            play   play   resume      resume
```

Tested:
- [x] v2.2.0 pre19
- [x] v2.2.0 pre20
- [x] v2.2.0 pre21

<sup>Note: Tested with PVR (no seeking possible) and non-weekly timer</sup>

### TC 4.3. Nested timers w/o resume and w/ former media
#### TC 4.3.1. T1 and T2 are no resumers
```
Media 1 |---------|
Timer 1           |-------------------------X
Timer 2                  |------X

t       |----M1---|--T1--|--T2--|-----------|---------------->
        t0        t1 t2  t3 t4  t5   t6     t7   t8
Player            play   play   stop
```

Tested:
- [x] v2.2.0 pre20
- [ ] v2.2.0 pre21 - After T2 ends it continues playing T2 (FAIL), after T1 ends it stops (OK)
- [x] v2.2.0 pre22 - Unit test OK, manual test OK

<sup>Note: Tested with PVR (no seeking possible) and non-weekly timer</sup>

#### TC 4.3.2. Only T1 is no resumer
```
Media 1 |---------|
Timer 1           |-------------------------X
Timer 2                  |------R

t       |----M1---|--T1--|--T2--|---T1------|---------------->
        t0        t1 t2  t3 t4  t5   t6     t7   t8
Player            play   play   resume      stop
```

Tested:
- [x] v2.2.0 pre20
- [x] v2.2.0 pre21

<sup>Note: Tested with PVR (no seeking possible) and non-weekly timer</sup>

#### TC 4.3.3. Only T2 is no resumer
```
Media 1 |---------|
Timer 1           |-------------------------R
Timer 2                  |------X

t       |----M1---|--T1--|--T2--|-----------|---------------->
        t0        t1 t2  t3 t4  t5   t6     t7   t8
Player            play   play   stop
```

Tested:
- [ ] v2.2.0 pre20 -> After T1 ends finally it restarts T2 --> Fix: Changed behaviour, i.e. T2 stops playing
- [ ] v2.2.0 pre21 - ident. TC 4.3.1 - After T2 ends it continues playing T2 (FAIL), after T1 ends it stops (OK)
- [x] v2.2.0 pre22 - Unit test OK, manual test ok

<sup>Note: Tested with PVR (no seeking possible) and non-weekly timer</sup>

#### TC 4.3.4. Only T2 is no resumer but w/o former media
```
Timer 1           |-------------------------R
Timer 2                  |------X

t       |----M1---|--T1--|--T2--|-----------|---------------->
        t0        t1 t2  t3 t4  t5   t6     t7   t8
Player            play   play   stop
```

Tested:
- [ ] v2.2.0 pre20 - ident. TC 4.3.3.
- [FAIL] v2.2.0 pre21 - ident. TC 4.3.1 - After T2 ends it continues playing T2 (FAIL), after T1 ends it stops (OK)
- [x] v2.2.0 pre22 - Unit test OK, manual test OK

<sup>Note: Tested with PVR (no seeking possible) and non-weekly timer</sup>

#### TC 4.3.5. Only T1 is no resumer but w/o former media
```
Timer 1           |-------------------------X
Timer 2                  |------R

t       |----M1---|--T1--|--T2--|---T1------|---------------->
        t0        t1 t2  t3 t4  t5   t6     t7   t8
Player            play   play   resume      stop
```

Tested:
- [x] v2.2.0 pre20
- [x] v2.2.0 pre21

<sup>Note: Tested with PVR (no seeking possible) and non-weekly timer</sup>

### TC 4.4. Nested timer w/ playlist and w/ resume and w/ former media
```
Media 1 |---------|                         |---------------->   (PVR)
Timer 1           |--+-----+-----+---+------R                    (Playlist)
Timer 2                  |------R                                (Single track)

t       |----M1---|--T1--|--T2--|---T1------|------M1-------->
        t0        t1 t2  t3 t4  t5   t6     t7   t8
Player            play   play   play+seek   resume
```

Tested:
- [x] v2.2.0 pre19
- [x] v2.2.0 pre20
- [x] v2.2.0 pre21

<sup>Note: Tested with 372non-weekly timer</sup>
