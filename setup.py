from setuptools import setup, find_packages

setup(
    name='indico.epayment.sixpay',
    version='0.0.1',
    description='Indico EPayment Sub-Plugin to use SixPay services',
    author='Max Fischer',
    author_email='max.fischer@kit.edu',
    entry_points={'indico.ext': ['EPayment.sixPay = sixPay', ], },
    packages=find_packages(),
    package_data={'sixPay': ['tpls/*.tpl']},
    zip_safe=False,  # TODO: DEBUG only
)
