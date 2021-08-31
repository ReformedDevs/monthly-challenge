# The Reformed Dev's September Challenge

The TRD challenge for the month of September is to create an AI that can win a
game of [minesweeprs](https://en.wikipedia.org/wiki/Minesweeper_(video_game)).
The winner will be whoever can create an AI that successfully completes all
game boards given in the fastest _average_ time. Any game boards that are not
successfully completed will exclude the AI's times from the ranking. The
person with the fastest AI at 23:59:59 on 2021-09-30 will be the winner of the
September Challenge.

Each AI will be run five times, against five separate game boards. The same
five game boards will be used for all entries.

## Entry Requirements

PLEASE NOTE THAT I HAVE NOT YET FINALIZED THE KUBERNETES MANIFEST SPECIFICS.
THIS SHOULD NOT IMPEDE YOUR ABILITY TO DEVELOP YOUR AI, MERELY YOUR ABILITY
TO RUN OFFICIAL TIMES.

To submit an entry, create a PR against this repository. Copy the `example.yaml`
File in the `./deploy/entries/` directory. Rename the file to your _GitHub_
username and [TODO]. Your entry will need to be bundled in a Docker image.
Please open an issue in this repository if you require assistance with either
the Docker image creation or setting up the Kubernetes manifest for your
entry.

Each entry should accept either the following `ENV` or arguments:

``` bash
SERVER or --server
WIDTH or --width
HEIGHT or --height
DIFFICULTY or --difficulty
SEED or --seed
```

This input will be used to construct the full URI to get the current round's
game board from the API server. Your AI will then play the game and then
return the following JSON:

``` json
'elapsed_time_in_ms': 123456789,
'final_game_state': '<GAME STATE WITHOUT NEWLINES>'
```

Please notice that the `final_game_state` should not include any newlines.

When measuring time, please start your timing as the very first possible line
in your program, and end your time as the very last line _before_ returning.
The _only_ line other than your return statement which is allowed to follow
the end of the timer is the _creation_ of the JSON. Please _do not_ make _any_
function calls in your return statement. In python the above might look similar
to:

``` python
def main():
    ...
    
    
if __name__ == "__main__":
    start = time.now()
    x = main()
    elapsed = time.now() - start
    print(json.dump({...}))
```

There will be a hard cap on run time, as well as CPU and mem limits. I have notice
determined these yet, but I will update this when it was been determined. I would
appreciate it if you did not knowingly submit entries which consistently run past
the upper bounds of the time limit, as this is just wasted cycles on my cluster.

## Minesweeper API

For the minesweeper logic we will be using the [`mineswepttd`](https://github.com/pard68/mineswepttd)
server. This is a stateless, RESTful server that handles the logic for the game
of minesweeper. The server will be bundled with your AI when it is tested, you
do not need to worry about implementing the server.

If there are any issues with the server, please submit an issue to the repo for
the `mineswepttd` server and I will address it there.

## Community

In an effort to foster a fair and enjoyable time from both the TRD Slack and
the TRD Facebook communities, please use the GitHub issues and the GitHub
discussion areas to communicate regarding this challenge when applicable.
For TRD members who only are on Facebook, the finer points of the
`monthly-challenge` infrastructure management wil be conducted on the TRD slack
instance, feel free to reach out for an invite if you would like to
contribute to the overarching infrastructure needs.  
