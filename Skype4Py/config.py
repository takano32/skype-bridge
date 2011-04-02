from configobj import ConfigObj

config = ConfigObj()
config.filename = "skype-lingr.conf"

config['lingr'] = {'verifier': 'hoge'}

config['arakawatomonori'] = {'skype': 'hoge', 'lingr': 'arakawatomonori'}
config['pirate'] = {'skype': 'foo', 'lingr': 'pirate'}

# config.write()

config = ConfigObj("skype-lingr.conf")

import pprint
pp = pprint.PrettyPrinter(indent = 4)

pp.pprint(config)
print config['arakawatomonori']['lingr']

