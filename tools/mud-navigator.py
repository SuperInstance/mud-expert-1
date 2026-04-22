#!/usr/bin/env python3
"""
MUD Navigator — Pathfinding for Plato rooms (v2).

Find the shortest path between any two rooms in the MUD.
Built by mud-scout-ccc-2 from the complete room map (v2 — 2026-04-23 rebuild).
"""
import json
import sys
from pathlib import Path
from collections import deque

# Try v2 first, fall back to v1
MAP_V2 = Path(__file__).parent.parent / "state" / "room-map-v2.json"
MAP_V1 = Path(__file__).parent.parent / "state" / "room-map.json"

def load_map():
    map_file = MAP_V2 if MAP_V2.exists() else MAP_V1
    with open(map_file) as f:
        return json.load(f)


def find_path(rooms_data, start, end):
    """BFS shortest path between two rooms."""
    if start not in rooms_data or end not in rooms_data:
        return None
    
    if start == end:
        return [start]
    
    visited = {start}
    queue = deque([(start, [start])])
    
    while queue:
        current, path = queue.popleft()
        
        room = rooms_data[current]
        # Handle both v1 (exits list) and v2 (exit_rooms list)
        exits = room.get("exit_rooms", room.get("exits", []))
        
        for exit_room in exits:
            if exit_room == end:
                return path + [exit_room]
            
            if exit_room not in visited and exit_room in rooms_data:
                visited.add(exit_room)
                queue.append((exit_room, path + [exit_room]))
    
    return None


def format_path(rooms_data, path):
    """Pretty-print a path with room names and taglines."""
    lines = []
    for i, room_id in enumerate(path):
        room = rooms_data.get(room_id, {})
        name = room.get("name", room_id)
        tagline = room.get("tagline", "")
        arrow = "→" if i < len(path) - 1 else "🏁"
        lines.append(f"  {arrow} {name} — {tagline}")
    return "\n".join(lines)


def main():
    if len(sys.argv) < 3:
        print("Usage: mud-navigator.py <from_room> <to_room>")
        print("Example: mud-navigator.py harbor ouroboros")
        print("\nKnown rooms (v2):")
        data = load_map()
        rooms = data.get("rooms", data)  # v2 wraps in "rooms", v1 doesn't
        for room_id in sorted(rooms.keys()):
            room = rooms[room_id]
            print(f"  {room_id:20s} — {room.get('tagline', '')[:50]}")
        sys.exit(1)
    
    start = sys.argv[1]
    end = sys.argv[2]
    
    data = load_map()
    rooms = data.get("rooms", data)
    
    if start not in rooms:
        print(f"❌ Unknown room: {start}")
        sys.exit(1)
    if end not in rooms:
        print(f"❌ Unknown room: {end}")
        sys.exit(1)
    
    path = find_path(rooms, start, end)
    
    if path is None:
        print(f"❌ No path found from {start} to {end}")
        sys.exit(1)
    
    print(f"\n🗺️  Path: {start} → {end}")
    print(f"   Distance: {len(path) - 1} moves\n")
    print(format_path(rooms, path))
    print(f"\n✅ Arrived at {rooms[end].get('name', end)}")


if __name__ == "__main__":
    main()
