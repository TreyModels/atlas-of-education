"""E14 actor knockouts + E15 state priorities, via the triad model's own necessity/lockin/state_motive designs."""
import json, os, sys, time
sys.path.insert(0, '/tmp/massrun/work/triad')
sys.path.insert(0, '/tmp/massrun/work/exp')
from triad.experiments import necessity, lockin
from triad.experiments_r4 import state_motive


def main():
    OUT = sys.argv[1]; REPS = int(sys.argv[2]); N = int(sys.argv[3]); W = int(sys.argv[4])
    t0 = time.time()
    print(f'triad: necessity reps={REPS} N={N}', flush=True)
    necessity(os.path.join(OUT, 'E14_necessity'), reps=REPS, workers=W, N=N, quick=False)
    print(f'triad: lockin', flush=True)
    lockin(os.path.join(OUT, 'E14_lockin'), reps=REPS, workers=W, N=N, quick=False)
    print(f'triad: state_motive', flush=True)
    state_motive(os.path.join(OUT, 'E15_state_motive'), reps=REPS, workers=W, N=N, quick=False)
    wall = time.time() - t0
    print(f'triad wall={wall:.0f}s', flush=True)
    json.dump(dict(eid='E14+E15', reps=REPS, N=N, wall=wall),
              open(os.path.join(OUT, 'run_meta.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
