from __future__ import annotations

import pytest

from rad.features.profile_cache import CappedSet, ProfileCache, WindowObservation


def test_capped_set_stops_growing_and_counts_overflow():
    s = CappedSet(2)
    assert s.add("a") and s.add("b")
    assert not s.add("a")  # duplicate, not overflow
    assert not s.add("c")
    assert list(s) == ["a", "b"] and len(s) == 2
    assert "c" not in s and s.overflow == 1


def test_capped_set_rejects_zero_cap():
    with pytest.raises(ValueError):
        CappedSet(0)


def test_commit_is_the_only_way_in():
    p = ProfileCache()
    obs = WindowObservation(0.0, dst_ips=("1.2.3.4",), dst_ports=(23,), domains=("a.example",))
    assert not p.has_ip("1.2.3.4")
    p.commit(obs)
    assert p.has_ip("1.2.3.4") and p.has_dst_port(23) and p.has_domain("a.example")
    assert p.windows_committed == 1


def test_profile_is_bounded():
    p = ProfileCache(max_ips=3, max_ports=2, max_domains=1)
    p.commit(WindowObservation(0.0, dst_ips=tuple(f"10.0.0.{i}" for i in range(10)),
                               service_ports=((1, 1), (2, 1), (3, 1))))
    stats = p.stats()
    assert (stats["ips"], stats["ips_overflow"]) == (3, 7)
    assert (stats["service_ports"], stats["service_ports_overflow"]) == (2, 1)
    # First-seen items win, so the result is deterministic.
    assert p.has_ip("10.0.0.0") and not p.has_ip("10.0.0.9")


def test_top_ports_by_count_then_port_number():
    p = ProfileCache(top_k_ports=3)
    p.commit(WindowObservation(0.0, service_ports=((443, 5), (80, 3), (8080, 3), (53, 1))))
    assert p.top_ports() == (443, 80, 8080)
    p.commit(WindowObservation(30.0, service_ports=((53, 10),)))
    assert p.top_ports() == (53, 443, 80)
