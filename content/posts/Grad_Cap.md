## The idea
When I graduated from university earlier this year, I wanted to decorate my cap in some CS-y way. So some sort of embedded project made sense. I thought about maybe attaching some LED lights that change color or intensity based off accelerometer readings, but then I saw these HUB75 RGB LED matrix displays on [Adafruit](https://www.adafruit.com/product/4732). They're the same type of display you seen used as billboards, in airport terminals, etc...

In order to control the display, I decided to go with a Teensy 4.1. There are attachments for [Raspberry Pis](https://www.adafruit.com/product/3211) and even all-in-one [ESP32 units](https://www.makerfabs.com/esp32-trinity.html). But I went with a Teensy because it's compact and can be used for other projects in the future. Instead of wiring a bare Teensy to the display (which would likely need 5V level shifters and be bulky), I used the [SmartLED shield](https://www.crowdsupply.com/pixelmatix/smartled-shield-for-teensy-4#products) which is designed to work with the helpful [SmartMatrix](https://github.com/pixelmatix/SmartMatrix/) library. One of the most common uses of the library is to display animated gifs, which I thought would be an easy way to display some cool graphics. 

## The build

In sum, the supplies I used were:
* 64x64 RGB LED Matrix with 3mm Pitch
* Teensy 4.1 (headers were pre-soldered, but you can solder your own)
* SmartLED Shield for Teensy 4
* 20,000 mAh USB power bank
* USB cables (preferably power-only)
* 4x4 Matrix Keypad
* microSD Card



I used Velcro strips to affix the panel and keypad to my graduation cap, and cut holes through the top in order to bring the wiring behind my neck.

## Results

