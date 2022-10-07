import ShrimpSouls as ss

u = ss.User("distractioncrab")

print(u.health)
print(u.attackers)
u.update_attackers("nothing")
print(u.attackers)
print(u.supporters)
u.update_supporters("someone")
print(u.supporters)

print(u.block)
u.stack_block()
print(u.block)
u.use_block()
print(u.block)
