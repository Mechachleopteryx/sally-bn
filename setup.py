from distutils.core import setup

setup(name="sallybn",
      version="1.0a",
      description="An Open-Source Framework for Bayesian Networks",
      author="David Saldana",
      author_email="dajulian@gmail.com",
      url="http://dsaldana.github.io/sallybn/",
      license="GPL",
      keywords="statistics, bayes",
      py_modules=["lib_sallybn"],
      scripts=["sallybn"],
      packages=["lib_sallybn", "lib_sallybn.drawer", "lib_sallybn.util", "lib_sallybn.disc_bayes_net",
        "resources",'libpgm', 'libpgm.CPDtypes'],
      package_data={'resources': ['gui/*.glade', 'gui/images/*.png', 'images/*.gif','images/*.png']}
)