# cbpi-powerrescaler
A plugin for CraftBeerPi that wraps a power controlled actor in another actor that rescales the power range of the base actor

  This plugin adds a ``RescaledActor`` that wraps another actor, and rescales the requested power
  linearly according the min and max power properties.

  This allows you to set a maximum power output for an over powered heater
  or to set a minimum power output for something like a pump that stalls below
  a certain power setting.

  Internal checking that the minimum power is less than the maximum power is done
  when the power is set. Errors in settings may not show up until the Actor is
  used.

  CraftBeerPi3 uses integers between 0 and 100 for the power settings for
  many actors, and so this plugin may cause quantization issues if the range
  between minimum and maximum power is small.
