from setuptools import setup, find_packages

setup(
    name='indico_sixpay',
    version='0.9.0',
    description='Indico EPayment Sub-Plugin to use SixPay services',
    author='Max Fischer',
    author_email='max.fischer@kit.edu',
    entry_points={'indico.ext': ['EPayment.sixPay = indico_sixpay', ], },
    packages=find_packages(),
    package_data={'indico_sixpay': ['tpls/*.tpl']},
    install_requires=['requests', 'indico>=1.2'],
    license='GPL',
    zip_safe=False,  # TODO: DEBUG only
)
