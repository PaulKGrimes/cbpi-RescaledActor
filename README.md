# cbpi-RescaledActor
A plugin for CraftBeerPi that wraps a power controlled actor in another actor that rescales the power range of the base actor

This plugin adds a ``RescaledActor`` that wraps another actor, and rescales the requested power
linearly according to the Minimum and Maximum Power properties.

This allows you to set a maximum power output for an over-powered heater
or to set a minimum power output for something like a pump that stalls below
a certain power setting.  Although the various PWM logic controllers allow you to
set a maximum power output, this may be useful with other controllers.

If you really want to, you can cascade multiple ``RescaledActor``s, and you setting
minimum and maximum values outside the 0-100% power range will work as long as
the values that are passed to a real actor are in the 0-100% range.

Internal checking that the minimum power is less than the maximum power is done
when the power is set. Errors in settings may not show up until the Actor is
used.

CraftBeerPi3 uses integers between 0 and 100 for the power settings for
many actors (e.g. the base GPIOPWM actor), and so this plugin may cause quantization
issues if the range between minimum and maximum power is small.  The ``RescaledActor``
itself uses floats, and so there shouldn't be any issues with internal quantization.
