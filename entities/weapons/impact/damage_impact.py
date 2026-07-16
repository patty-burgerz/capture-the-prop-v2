from entities.weapons.impact.impact_behavior import ImpactBehavior

class DamageImpact(ImpactBehavior):
    """
    Applies damage to the target player when a bullet hits.
    """

    def apply(self, bullet, target):
        target.take_damage(bullet.damage)