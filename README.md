# Project - Smart Bus Stop (ponto de ônibus inteligente)

This is a repository dedicated to the Smart Bus Stop project, made as final project for the MO629A_2024S2 (Internet of Things) class in IC - Unicamp. 
The goal of this project is to enhance the Unicamp Smart Campus project, adding some functionalities on the bus stops.


## Features

This project features are:

* Count how many people are waiting for a bus in a given bus stop using computer vision techniques
* Periodically send this people counter value to a IoT platform (Tago.IO) using LoRaWAN connectivity
* This project has a panic button in it. So, if a bus stop user feels in danger for some reason (health issues, security issues, etc.), the user can press this button and a panic event is trigerred. Then, the authorities are able to see this alert in project's dashboard and take the necessary actions to offer user help.
* Also, if a wi-fi connection is available where this project is located in, a Telegram message is sent to the authorities when panic button is pressed, in order to add a new layer / redundance to the panic buton event handling.


## How is this project organized?

In order to offer more modularity and make it easier to maintain the project's source-code, each major part of this project has been developed as a isolated module, which can work as a independent service.
The modules that compose this project are:

* Panic button module (folder: panic_button): module responsible for reading panic button state and generate panic button events.
* People detection (folder: people_detection_sw): module responsible for reading camera frames and count how many people are in the image frames. This module also generates people counter events, containing the number of people in bus stop.
* LoRaWAN connectivity (folder: lorawan): module responsible for configure LoRaWAN connectivity, receiving people counter and pannic button events and sending events o TagoIO IoT platform using LoraWAN messages for each event.
* TagoIO parser (folder: TagoIO): TagoIo parser


## Project documentation

The project documentation available so far consists of the project's presentation used in MO629A_2024S2 class.
This presentation is available in this repository, into "Apresentação" folder. 
Note: as this class and project members native languages are Portuguese, this presentation is only available in Portuguese.