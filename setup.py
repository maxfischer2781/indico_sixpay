from setuptools import setup, find_packages

setup(
    name='indico_sixpay',
    version='2.0.0pre',
    description='Indico EPayment Plugin for SixPay services',
    url='https://github.com/maxfischer2781/indico_sixpay',
    author='Max Fischer',
    author_email='maxfischer2781@gmail.com',
    entry_points={
        'indico.plugins': {
            'payment_sixpay = indico_sixpay.plugin:SixpayPaymentPlugin'
        }
    },
    packages=find_packages(),
    package_data={'indico_sixpay': ['tpls/*.tpl']},
    install_requires=['requests', 'indico>=2.0rc1'],
    license='GPLv3+',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Communications :: Conferencing',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    zip_safe=False,
    keywords='indico epayment six sixpay plugin',
)
