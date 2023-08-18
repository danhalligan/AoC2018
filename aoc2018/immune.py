import re
import math


class Group:
    def __init__(self, txt, type, number):
        pattern = "(\d+) units each with (\d+) hit points (?:\((.+)\) |)with an attack that does (\d+) (\w+) damage at initiative (\d+)"
        r1 = re.match(pattern, txt).groups()
        self.units = int(r1[0])
        self.hit_points = int(r1[1])
        self.attack_damage = int(r1[3])
        self.attack_type = r1[4]
        self.initiative = int(r1[5])
        self.weaknesses = []
        self.immunities = []
        self.selected = False
        self.type = type
        self.target = None
        self.number = number
        r2 = re.match(".+weak to (.+?)(;|\)).+", txt)
        if r2:
            self.weaknesses = r2.groups()[0].split(", ")
        r2 = re.match(".+immune to (.+?)(;|\)).+", txt)
        if r2:
            self.immunities = r2.groups()[0].split(", ")

    def effective_power(self):
        # the number of units in that group multiplied by their attack damage.
        return self.units * self.attack_damage

    def damage(self, defn):
        # An attacking deals damage equal to its effective power
        # If the defending group is immune to the attacking group's attack type, the defending group instead takes no damage
        # if the defending group is weak to the attacking group's attack type, the defending group instead takes double damage.
        if self.attack_type in defn.immunities:
            return 0
        elif self.attack_type in defn.weaknesses:
            return self.effective_power() * 2
        else:
            return self.effective_power()

    def damage_result(self, defn):
        # The defending group only loses whole units from damage;
        # damage is always dealt in such a way that it kills the most
        # any remaining damage to a unit is ignored.
        points = self.damage(defn)
        return min(defn.units, math.floor(self.damage(defn) / defn.hit_points))

    def valid_defender(self, defn):
        # An attacker can select a defender if of a different type, if
        # not already selected and if the attacker can deal damage
        return defn.type != self.type and not defn.selected and self.damage(defn) > 0


class Board:
    def __init__(self, file):
        set1, set2 = open(file).read().split("\n\n")
        sys = [
            Group(x, type="immune", number=i + 1)
            for i, x in enumerate(set1.splitlines()[1:])
        ]
        inf = [
            Group(x, type="infection", number=i + 1)
            for i, x in enumerate(set2.splitlines()[1:])
        ]
        self.groups = sys + inf

    def target_selection(self):
        # Each group attempts to choose one target
        # - in decreasing order of effective power
        # - in a tie, pick higher initiative
        self.groups.sort(key=lambda x: (-x.effective_power(), -x.initiative))

        # Attacking chooses enemy army to which it would deal the most damage
        # In tie choose defender with largest effective power then initiative.
        # If it cannot deal any defending groups damage, it does not choose a target.
        for attacker in self.groups:
            defenders = [x for x in self.groups if attacker.valid_defender(x)]
            if defenders:
                defenders = sorted(
                    defenders,
                    key=lambda x: (
                        -attacker.damage(x),
                        -x.effective_power(),
                        -x.initiative,
                    ),
                )
                attacker.target = defenders[0]
                attacker.target.selected = True

    def attack(self, verbose=False):
        for att in sorted(self.groups, key=lambda x: -x.initiative):
            if att.units > 0 and att.target:
                defn = att.target
                if verbose:
                    print(
                        f"{att.type} group {att.number} attacks defending group {defn.number} killing {att.damage_result(defn)} units"
                    )
                att.target.units -= att.damage_result(att.target)

        self.groups = [x for x in self.groups if x.units > 0]
        for x in self.groups:
            x.selected = False
            x.target = None

    def immune_groups(self):
        return [x for x in self.groups if x.type == "immune"]

    def infection_groups(self):
        return [x for x in self.groups if x.type == "infection"]

    def status_report(self):
        print("Immune System:")
        for x in sorted(self.immune_groups(), key=lambda x: x.number):
            print(f"Group {x.number} contains {x.units} units")
        print("Infection:")
        for x in sorted(self.infection_groups(), key=lambda x: x.number):
            print(f"Group {x.number} contains {x.units} units")

    def add_boost(self, boost):
        for x in self.immune_groups():
            x.attack_damage += boost

    def play(self, verbose=False):
        while len(self.immune_groups()) and len(self.infection_groups()):
            if verbose:
                print()
                self.status_report()
                print()
            self.target_selection()
            self.attack(verbose=verbose)
        winner = "immune" if len(self.immune_groups()) else "infection"
        return {"winner": winner, "score": sum(x.units for x in self.groups)}
