from setuptools import setup

setup(name = 'bioport_repository',
      packages = ['bioport_repository', 
                  'bioport_repository/similarity',
                 ],

      install_requires=['gerbrandyutils',
                        'PIL',
                        'biodes',
                       ],
      )
