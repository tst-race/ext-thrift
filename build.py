#!/usr/bin/env python3

#
# Copyright 2023 Two Six Technologies
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
Script to build Apache Thrift for RACE
"""

import logging
import os
import race_ext_builder as builder


def get_cli_arguments():
    """Parse command-line arguments to the script"""
    parser = builder.get_arg_parser("thrift", "0.12.0", 1, __file__)
    parser.add_argument(
        "--boost-version",
        default="1.73.0-1",
        help="Version of Boost dependency",
        type=str,
    )
    parser.add_argument(
        "--openssl-version",
        default="1.1.1l-1",
        help="Version of OpenSSL dependency",
        type=str,
    )
    return builder.normalize_args(parser.parse_args())


if __name__ == "__main__":
    args = get_cli_arguments()
    builder.make_dirs(args)
    builder.setup_logger(args)

    builder.install_packages(args, [
        "bison=2:3.5.1*",
        "flex=2.6.4*",
    ])
    builder.install_ext(args, [
        ("boost", args.boost_version),
    ])
    if args.target.startswith("android"):
        builder.install_ext(args, [
            ("openssl", args.openssl_version),
        ])
    else:
        builder.install_packages(args, [
            ("libssl-dev", "1.1.1*", True),
            ("zlib1g-dev", "1:1.2.11*", True),
        ])

    builder.fetch_source(
        args=args,
        source=f"https://github.com/apache/thrift/archive/refs/tags/v{args.version}.tar.gz",
        extract="tar.gz",
    )

    source_dir = os.path.join(args.source_dir, f"thrift-{args.version}")
    env = builder.create_standard_envvars(args)

    logging.root.info("Configuring build")
    if args.target.startswith("linux"):
        builder.execute(args, [
            "cmake",
            f"-H{source_dir}",
            f"-B{args.build_dir}",
            f"-DCMAKE_STAGING_PREFIX={args.install_dir}",
            f"-DCMAKE_INSTALL_PREFIX={args.install_prefix}",
            "-DWITH_CPP=ON",
            "-DWITH_JAVA=OFF",
            "-DWITH_PYTHON=OFF",
            "-DBUILD_EXAMPLES=OFF",
            "-DBUILD_TESTING=OFF",
            "-DBUILD_TUTORIALS=OFF",
        ], env=env)

    elif args.target.startswith("android"):
        builder.execute(args, [
            "cmake",
            f"-H{source_dir}",
            f"-B{args.build_dir}",
            f"-DCMAKE_STAGING_PREFIX={args.install_dir}",
            f"-DCMAKE_INSTALL_PREFIX={args.install_prefix}",
            f"-DCMAKE_TOOLCHAIN_FILE={os.environ['ANDROID_NDK']}/{args.target}.toolchain.cmake",
            "-DWITH_CPP=ON",
            "-DWITH_JAVA=OFF",
            "-DWITH_PYTHON=OFF",
            "-DBUILD_EXAMPLES=OFF",
            "-DBUILD_TESTING=OFF",
            "-DBUILD_TUTORIALS=OFF",
        ])

    logging.root.info("Building")
    builder.execute(args, [
        "cmake",
        "--build",
        args.build_dir,
        "--target",
        "install",
        "--",
        "-j",
        args.num_threads,
    ])

    builder.create_package(args)
