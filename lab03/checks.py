from helpdesk_conn import get_redis
from models import *

r = get_redis()

def urgent_list():
    return r.zrevrange(PRIORITY_Q, 0, 4, withscores=True)

def agent_workload(aid):
    return r.hget(agent_key(aid), "load")

def invariants_ok():
    ok = True
    for tid in r.smembers(ALL_TICKETS):
        aid = r.hget(ticket_key(tid), "assigned_agent")
        if aid and not r.sismember(agent_open(aid), as_member_ticket(tid)):
            print("Invariant failed: ticket", tid, "missing in agent open set", aid)
            ok = False
    for tid in r.smembers(ALL_TICKETS):
        st = r.hget(ticket_key(tid), "status")
        if st == "closed" and r.zscore(PRIORITY_Q, as_member_ticket(tid)) is not None:
            print("Invariant failed: closed ticket", tid, "still in priority ZSET")
            ok = False
    for key in r.scan_iter(IDX_USER_EMAIL + ":*"):
        email = key.split(":", maxsplit=3)[-1]
        uid = r.get(key)
        if r.hget(user_key(uid), "email") != email:
            print("Invariant failed: email index mismatch for", email)
            ok = False
    return ok

if __name__ == "__main__":
    print("Urgent (top 5):", urgent_list())
    print("Agent 1 load:", agent_workload("1"))
    print("Agent 2 load:", agent_workload("2"))
    print("Agent 3 load:", agent_workload("3"))
    print("Consistency OK?:", invariants_ok())
