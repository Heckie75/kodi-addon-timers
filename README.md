# kodi-addon-heckies-timer
Powerful timers for KODI


I wanted to have a Kodi addon that is a sleep timer, a doze timer, has several other timer slots and combines it with fading volume in and out over a certain period. Since I haven't found it I decided to program it by myself. 

The result is a powerful timer addon.  

## Overview of features:
* 10 timer slots. All of them can be quickly set up by using context menu
* 2 additional slots for sleep and doze timers with 5-clicks-setup 
* Timers can play any ressource that it available in Kodi, e.g. music, video files, TV/radio programs, ressources from 3rd party plugins, e.g. Zattoo channels. 
* Different schedule modes: once, everyday, Mon-Fri, Fri-Sat, Sat-Sun, Sun-Thu, Mon-Thu, specific weekday
* Date change is supported, e.g. from 23:30 (p.m.) until 1:30 (a.m.) 
* Two end modes, i.e. duration or specific time
* Actions related to media: Play at start and stop at end, just play at start, stop immediately at start, just stop at end, do nothing with media
* Linear fading in timer period: fade-in, fade-out, no fading. Min and max volume can be set for each timer
* Custom label for timer
* After KODI startup timers, that are in period, start retroactivly altought KODI was not running at start time. Fading volume is calculated correctly.
* Feature in order to prevent Windows to start screensaver and lock screen

## Install kodi plugin / addon
First of all download the plugin archive file, i.e. [script.service.heckies.timer.zip](/script.service.heckies.timer.zip)

You must extract this archive in the Kodi plugin folder
```
# change to kodi's addon directory
$ cd ~/.kodi/addons/

# extract plugin
$ tar xzf ~/Downloads/script.service.heckies.timer.zip
```

After you have restarted Kodi you must activate the plugin explicitly. 
1. Start Kodi
2. Go to "Addons" menu
3. Select "User addons"
4. Select "Service" addons, select "Heckies timers" and activate it

## Timers in action

### 1. Snooze timer

Imagine that you want to have a nap and want to be awaken in 15 minutes. You can right-clicking any resource in KODI, e.g. some musik file, and pick it in order to setup a timer. In case of the "nap"-situation you pick a file and select the snooze timer. The settings dialog opens as follows:  

<img src="script.service.heckies.timer/resources/assets/screen1.png?raw=true">

By default the starting time is the current time plus 15 minutes. You can change it here. 

The snooze timer has no end time. Therefore it just starts the selected media. 

After you have saved the settings the timer is running. In 15 minutes the picked file will be played automatically. 


### 2. Sleep timer 

Most radio clocks have a sleep timer. The sleep timer is very simular. The sleep timer stops playing your media after some time. However, the plugin also allows you to fade the volume while it is playing. You can set the high volume, which is the volume at the beginning of the period, and the low volume which is the volume at the end. 

<img src="script.service.heckies.timer/resources/assets/screen2.png?raw=true">

The time is of type "Stop media at end". There is no action at when the timer starts. Make sure that you already play some file. 


### 3. Timer slots

In addition to the snooze timer and the sleep timer (actually normal timer slots but named) there are another 10 timer slots that you can program. 

<img src="script.service.heckies.timer/resources/assets/screen3.png?raw=true">

Let's take a look at the settings of each timer slot.

#### a. "Start time" 

This is the time when the timer starts its action.

#### b. "End" type

There are three options for the end:

i. "No" - which means that you won't define an end. In this case the timer just has a start action. Since there is no specific end it won't have an interval as well.  

ii. "Time"" - You will define a specific time, e.g. 20:15, when the timer ends. According the specified start time the timer runs in a period.

iii. "Duration" - In comparison to a dedicated end time the "Duration" option allows you to specify a duration in hours and minutes. The plugin calculates the end time by adding the duration to the start time. 

#### c. "Action"

The timer plug-in comes with several different action, i.e. 

i. "Just start media"

After the starting time has been reached the timer starts to play the given media. There won't be an action after the end has been reached so that KODI continues playing the media file. 

**Recommendation:** It seems to be hard to select the right media location. I recommend to select the media location by browsing your library, select a media, open the context menu by right-clicking the ressource (or press "c" key) and assign the selected ressource to a timer.

**Note:** The timer is not limited to media files. For instance, I am using the timer also in combination with my "Pulse-Audio Sink Setter" plugin, which allows me to switch the audio sink to a bluetooth device at a specific time, e.g. in the morning I want to play music on my bluetooth speakers in the kitchen.

**ii. "Play media (and stop at end)" type**

In comparison to the previuos option the timer will stop playing the media after the end time has been reached.

<img src="script.service.heckies.timer/resources/assets/screen4.png?raw=true">

iii. "Do nothing with media" type**

This option neither starts media nor stops media. You maybe ask: "What is it for?". The answer is that this kind of timer can be used in combination with volumne fading options, e.g. if you just want to reduce the volume in the evening hours - in order to do your neighbours a favor -  while you are already listing to something.  

iv. "Stop media at end" type

This option is simular to option iii. but it stops media at the end. This option should be combined with fading as well. See below.  


v. "Stop immediately"

This is the right option if you just want that some media that is already running will be stopped. 

**NOTE:** This stop action is at the start time of the timer

d. "Volume settings"

This timer plugin allows you to fade in and fade out the volume during timer's runtime. 

Note: The section "Volume settings" is not available for end type "No" since it is required to have a period. 

There are three fading options, i.e. 

i. "Off" - There is no fading

ii. "Fade in" - The plugin switches the volume to the "low volume" value when the timer starts and fades in (linear) to the "high volume" value until the given end

iii. "Fade out" - The plugin switches the volume to the "high volume" value when the timer starts and fades out to the "low volume" value until the given end
 
<img src="script.service.heckies.timer/resources/assets/screen5.png?raw=true">
