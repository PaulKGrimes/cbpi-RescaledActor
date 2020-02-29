from modules import cbpi
from modules.core.props import Property
from modules.core.hardware import ActorBase

@cbpi.actor
class RescaledActor(ActorBase):
    """An actor that wraps a base actor, and rescales the requested power
    linearly according to the min and max power properties.

    This allows you to set a maximum power output for an over powered heater
    or to set a minimum power output for something like a pump that stalls below
    a certain power setting.

    CraftBeerPi3 uses integers between 0 and 100 for the power settings for
    many actors, and so this plugin may cause quantization issues if the range
    between minimum and maximum power is small.
    """
    base = Property.Actor(label="Base Actor", description="Select the actor you would like to rescale")
    min_power = Property.Number("Minimum Power (%)", True, 99, description="The minimum output power of the actor when switched on. Use with caution on heaters!")
    max_power = Property.Number("Maximum Power (%)", True, 100, description="The maximum output power of the actor when switched on.")
    timeout = Property.Number("Notification duration (ms)", True, 5000, description="0ms will disable notifications completely")

    def init(self):
        # Where should we check that maximum is greater than minimum?
        # using set_power method for now, but it should be when min and max are set
        # on closing settings dialog
        pass

    def set_power(self, power):
        """Set the power as a percentage of the range between minimum and maximum power"""
        self.api.actor_power(int(self.base), power=self.rescale_power(power))

    def rescale_power(self, power):
        """Calculate the rescaled power from the requested power"""
        # We carry out the maths in a standalone function so that on and set_power
        # can use it

        # If power supplied is None, return our own power, so that base actor is
        # controlled to our power. If our power hasn't been set yet, set it to 100.0
        if power is None:
            try:
                power = self.power
            except AttributeError:
                try:
                    power = self.base.power
                except AttributeError:
                    power = None

        min_power = float(self.min_power)
        max_power = float(self.max_power)

        if min_power > max_power:
            self.api.notify(headline="Invalid Settings",
                message="Minium power is set to a value greater than the maximum power",
                timeout=self.timeout,
                type="danger")
            raise UserWarning("Minimum power is set to a value greater than maximum power")

        if min_power == max_power:
            raise UserWarning("Maximum and minimum power are equal")
            self.api.notify(headline="Invalid Settings",
                message="Minimum power is set equal to the maximum power",
                timeout=self.timeout,
                type="danger")
            raise UserWarning("Minimum power is set equal to maximum power")

        rescaled_power = min_power + (max_power - min_power)/100. * power

        return rescaled_power

    def off(self):
        """Switch the actor off"""
        self.api.switch_actor_off(int(self.base))

    def on(self, power=None):
        """Switch the actor on"""
        self.api.switch_actor_on(int(self.base), power=self.rescale_power(power))
