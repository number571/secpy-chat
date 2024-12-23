<img src="images/secpy_chat_logo.png" alt="secpy_chat_logo.png"/>

<h2>
	<p align="center">
    <strong>
      Console messenger with end-to-end encryption
   	</strong>
	</p>
	<p align="center">
    <a href="https://github.com/topics/python">
      <img src="https://img.shields.io/badge/Python-v3-1f425f.svg" alt="Python" />
		</a>
    <a href="https://github.com/number571/go-peer/blob/master/LICENSE">
      <img src="https://img.shields.io/github/license/number571/go-peer.svg" alt="License" />
		</a>
    <a href="https://github.com/number571/go-peer">
      <img src="https://raw.githubusercontent.com/number571/go-peer/refs/heads/master/images/go-peer_badge.svg" alt="Go-Peer" />
		</a>
	</p>
	About project
</h2>

The application `secpy_chat` allows you to communicate securely (using end-to-end encryption) using HLT and HLE applications (v1.7.7). This is an example of how it is possible to write client-safe applications for the Hidden Lake environment without being based on the Go programming language (the main language for writing Hidden Lake applications).

> More information about Secpy-Chat in the [habr.com/ru/articles/782836/](https://habr.com/ru/articles/782836/ "Habr Secpy-Chat")

## Dependencies 

```bash
$ pip3 install -r requirements.txt
```

## Config structure

```
"hlt_host" address of the HLT service
"hle_host" address of the HLE service
```

```yaml
hlt_host: localhost:9582
hle_host: localhost:9551
```

## How it works

<p align="center"><img src="images/secpy_chat.gif" alt="secpy_chat.gif"/></p>
<p align="center">Figure 1. Chat node1 with node2.</p>

The application connects to two services at once: [HLE](https://github.com/number571/hidden-lake/tree/master/cmd/hle) and [HLT](https://github.com/number571/hidden-lake/tree/master/cmd/hlt). The first service makes it possible to encrypt and decrypt messages. The second service allows you to send and receive encrypted messages from the network. In this case, the secpy_chat is guided only by the interfaces of the services, representing the frontend component.

## Example 

Build and run services HLT, HLE
```bash
$ cd example
# install HLE, HLT
$ make install
# build & run
$ make 
```

Run client#1
```bash
$ cd example/node1
$ python3 main.py
> /friend Alice
# waiting client#2
> hello
> [Bob]: world!
```

Run client#2
```bash
$ cd example/node2
$ python3 main.py
> /friend Bob
# waiting client#1
> [Alice]: hello
> world!
```
