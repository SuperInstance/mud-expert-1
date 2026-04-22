#!/usr/bin/env python3
"""
MUD Navigator — Pathfinding for Plato rooms.

Find the shortest path between any two rooms in the MUD.
Built by mud-expert-resident-1 from the complete room map.
"""
import json
import sys
from pathlib import Path
from collections import deque

MAP_FILE = Path(__file__).parent.parent / "state" / "room-map.json"


def load_map():
    with open(MAP_FILE) as f:
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
        
        for exit_room in rooms_data[current]["exits"]:
            if exit_room == end:
                return path + [exit_room]
            
            if exit_room not in visited:
                visited.add(exit_room)
                queue.append((exit_room, path + [exit_room]))
    
    return None


def format_path(rooms_data, path):
    """Pretty-print a path with room names and taglines."""
    lines = []
    for i, room_id in enumerate(path):
        room = rooms_data[room_id]
        arrow = "→" if i < len(path) - 1 else "🏁"
        lines.append(f"  {arrow} {room['name']} — {room['tagline']}")
    return "\n".join(lines)


def main():
    if len(sys.argv) < 3:
        print("Usage: mud-navigator.py <from_room> <to_room>")
        print("Example: mud-navigator.py harbor ouroboros")
        print("\nKnown rooms:")
        data = load_map()
        for room_id in sorted(data["rooms"].keys()):
            room = data["rooms"][room_id]
            print(f"  {room_id:20s} — {room['name']}")
        sys.exit(1)
    
    start = sys.argv[1]
    end = sys.argv[2]
    
    data = load_map()
    rooms = data["rooms"]
    
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
    print(f"\n✅ Arrived at {rooms[end]['name']}")


if __name__ == "__main__":
    main()
