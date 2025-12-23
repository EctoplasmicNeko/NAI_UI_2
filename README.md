Hello, and thanks for checking out NAI UI 2. NAI UI 2 is a desktop UI app for the NovelAI image generation model, with a strong focus on allowing the user to define and reuse characters, while also aiming to provide a bit more personality. A number of other features are also planned for future release. 

GETTING STARTED:
To get started, download the latest build from the Releases section and extract the zip file to a location of your choice, then double click the included .exe to launch (no install required).

API KEY:
To use NAI UI 2, you will require a NovelAI API key. Generate this key from your user settings page on the NovelAI website and paste it into the Settings tab within NAI UI 2,
<img width="1201" height="761" alt="API" src="https://github.com/user-attachments/assets/f3739249-ae74-4269-b01a-1d17ebf3151e" />
<img width="386" height="388" alt="243324" src="https://github.com/user-attachments/assets/bb0a8d98-b0cd-4fe0-b465-b85d1b0ad73d" />

USING NAI UI 2
With your API Key in the correct box, you can now start using the app.

There is no 'Generate' button - to start an action, click the open area in the centre of the app (it's a big button).

<img width="377" height="388" alt="parameters" src="https://github.com/user-attachments/assets/8dec9472-a4c6-4c99-8472-590d3a078836" />

The Parameters tab allows for the setting of image generation parameters. Most of the settings here will be familiar to those who have used NovelAI or other image gen's before. The scroll at the top allows access to parameters for Emotion and Colorize tools. On the right is set tracker (more on this in the workflow tab section) and buttons that allow you to quickly return to zero/disabled for some functions.

<img width="381" height="391" alt="image" src="https://github.com/user-attachments/assets/0a1bcc58-d6e9-4d00-8a9b-d74c00320bea" />

The Prompt tab is for setting the global prompt for image generation tasks, as well as choosing from negative and positive quality presets. The 'P' button will cause the main prompt to be shown. The 'Q' button will show the selected quality preset, allowing you to temporarilly change it without redefining the preset. Currently, users cannot define additional presets though the UI (though can by editing the relevant JSON file). This is also where you choose how many character slots you wish to use. NAI UI 2 currently supprts between 0 and 5 character slots per generation.

<img width="381" height="392" alt="image" src="https://github.com/user-attachments/assets/0b59ac25-1e9a-4adf-935e-4f1da9a7774a" />

The workflow tab controls a number of additional functions, such as automatic parameter adjustment, character cycling and workflow. 
Generate, Upscale and Directors Tools tasks can be queued to occur sequentially by adding them to the task list, allowing you to easilly perform a more complex workflow without having to move to different menus or press different buttons. 

Loops and Sets allow you to define the number of operations in a task, which tie in to other automated adjustment settings elsewhere. Loops represent the number of operations to be called, and sets are groups of loops. To use NAI UI 2 'normally', set these to 1. Setting Sets to 0 will set the number of sets to the number of characters you have that meet the filter criteria. When this mode is set, the filter panel will be available, allowing you to select up to 3 character tags to filter by. 

Below this is a panel of buttons that allows you to define how outputs will be sorted in the Outputs folder. By default, all outputs will be deposited into the main output folder. By selecting these buttons, you can have the app create subfolders by date, by whatever character is in character slot 1, and by a set name. If the set name option is selected, an input field will appear where you can define the folder name. 

Note that in compliance with the NovelAI TOS, none of the automation functions in NAI UI 2 allow for autonomous image creation. All actions require the user to initiate the action by clicking the centre area.

<img width="383" height="390" alt="image" src="https://github.com/user-attachments/assets/58a4d5b9-7eef-44b6-bbc9-67bfd1323959" />

The modifiers tab will allow for autonomous parameter adjustment and randomization. These functions are currently in development and are not enabled.

<img width="384" height="387" alt="image" src="https://github.com/user-attachments/assets/2cceb16c-4c05-45d3-97d1-24a62a6108e7" />

The settings tab allows for setting adjustments:<br>
<b>Manage Characters</b> - Opens character management window, see below.<br>
<b>Manage Presets</b> - will allow for size and quality preset definition in the UI. Currently not implimented.<br>
<b>Manage Wildcards</b> - will allow for definition of wildcard keywords and values. Currently not implimented.<br>
<b>Manage Assistants</b> - For OAI Assistant integration (characters can react to your image). Not yet implimented.<br>
<b>Generate</b> - runs a 1 loop, 1 set generate task. Will be removed in future.<br>
<b>Test</b> - Button for dev assist. Does nothing.<br>
<b>Species bar</b> - Toggles the species icon bar. You can disable it if your not into kemonomimi.<br>
<b>Character Fluff Tab</b> - toggles between full and minimal character tab if you prefer a more utilitarian UI.<br>
<b>Embed references toggle</b> - Allows character references to be stored in image metadata. Increases the file size by alot.<br>
<b>Character Sorting</b> - Adjusts how character lists are sorted, by alphabetical name, age of character status. Status sorts based on 'main', 'supporting' and 'minor' character tags.<br>
<b>Write Hydrus Sidecars</b> - tasks will also write a Hydrus Network compatible sidecar .txt file. Currently, this sidecar lists the characters and image orientation. This feature will be expanded in future.<br>

