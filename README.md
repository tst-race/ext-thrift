# Apache Thrift for RACE

This repo provides scripts to custom-build the
[Thrift library](https://boost.org) for RACE.

## License

The Thrift library is licensed under the Boost Software License 1.0.

Only the build scripts in this repo are licensed under Apache 2.0.

## Dependencies

Thrift has dependencies on the following custom-built libraries:

* Boost
* OpenSSL (for Android)

## How To Build

The [ext-builder](https://github.com/tst-race/ext-builder) image is used to
build Thrift.

```
git clone https://github.com/tst-race/ext-builder.git
git clone https://github.com/tst-race/ext-thrift.git
./ext-builder/build.py \
    --target linux-x86_64 \
    ./ext-thrift
```

## Platforms

Thrift is built for the following platforms:

* `linux-x86_64`
* `linux-arm64-v8a`
* `android-x86_64`
* `android-arm64-v8a`

## How It Is Used

Thrift is a dependency for the Jaeger Client custom-built library.
