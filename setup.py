# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name="asset_bundles",
    version="0.1.3",
    packages=["asset_bundles", "asset_bundles.management",
              "asset_bundles.management.commands",
              "asset_bundles.templatetags"],
    package_data={
        "asset_bundles": ["yuicompressor-2.4.6.jar"]
    },
    install_requires=[
        "django",
    ],
    author="Viktor Kotseruba",
    author_email="barbuzaster@gmail.com",
    description="simple clone of django_assets compatible with "
                "django 1.3 and staticfiles",
    license="MIT",
    keywords="web django",
)
