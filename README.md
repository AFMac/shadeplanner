# shadeplanner
This tool was built to aid in planning small stained glass lampshade builds like those depicted here:

![glasses](https://github.com/user-attachments/assets/9de1493f-828e-488a-946d-39e0a19a96bf)

It uses `matplotlib` for visualization and some trigonometry, providing a tool allowing a user to dynamically modify geometric features and provide feedback on how large individual pieces of glass will need to be to make a lampshade.

# Execution
This is a single python script that can be run natively in Python, or built as a standalone executable with a tool like `Pyinstaller`.

# Usage
**Note:** Upon opening, the tool defaults to full screen mode to ensure visibility.  To exit, simply press the "f" key to return to a windowed view.

<img width="795" height="511" alt="image" src="https://github.com/user-attachments/assets/cafb4cc2-699f-4e4a-b0bc-52e26d4b4d66" />

Use is relatively straightforward.  Sliders at the bottom of the screen are used to modify size of the lamp base (the glass) as well as the lampshade itself.  This includes the ability to change how many sides the lampshade will have.  Units should be interpreted as metric (centimeters).  In general:

- The visualization presented is intended to represent a glass (skinny cylinder is the "stem", and the larger cylinder is the "bowl" of the glass), with the lampshade resting on top.  The red dots show a calculation of where the rim of the glass will make contact with the interior of the lampshade.

- Start by setting the slider for "Glass Radius".  This should be interpreted as the radius of the top (rim) of the glass being used for the base of the lamp.
   - Note that values at the top of the screen will change as the slider is moved.  More on this below.
 - Next, modify the "Shade bottom" and "Shade top" sliders until the lampshade achieves a desirable look.
   - Key here is the "Height of glass covered" figure presented at the top of the screen.  This represents how much of the glass "bowl" would be covered by the lampshade if looking from the side of the glass.  So, if the "bowl" of the glass is 3cm deep and the user desires the lampshade to cover the glass, make sure that the "Height of glass covered" figure is at least 3.0
   - Once the desired look and height are achieved, make note of the three separate length measures.  These represent measurements for individual glass panes of the lampshade itself.  So, "shade top length" indicates how wide the pane will be at the top, "shade bottom length" how wide at the bottom, and "shade length" is how long each pane must be (measured from the middle of each pane at top and bottom, *not* along the diagonal).

Note that these measures are intended to provide a close approximation for planning.  I strongly suggest using this to decide on a design, and use the proposed measures to generate a prototype with cardstock or cardboard to validate before cutting glass.  Enjoy!

