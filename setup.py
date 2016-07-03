import setuptools

setuptools.setup(
        install_requires=['requests'],
        author = 'Caleb Boylan',
        name = 'zendeskhc',
        description = 'Python module for interacting with the Zendesk Help Center API',
        author_email = 'calebboylan@gmail.com',
        url = 'https://github.com/squidboylan/zendeskpy',
        version = '0.4.0',
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: Apache Software License',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
        ],
        packages=setuptools.find_packages(),
)
