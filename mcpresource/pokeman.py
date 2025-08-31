import httpx
from fastmcp import FastMCP
from fastmcp.exceptions import ResourceError

# Use the same FastMCP instance as main.py
mcp = FastMCP("mcpresource")

# some pokemon for quick demonstration
STARTERS = {
    "1": "Bulbasaur",
    "2": "Ivysaur",
    "3": "Venusaur",
    "4": "Charmander",
    "5": "Charmeleon",
    "6": "Charizard",
    "7": "Squirtle"
}


@mcp.resource("pokemon://pokemon/{pokemon_id}")
async def get_pokemon(pokemon_id: str) -> dict:
    """Get detailed information about a specific Pokemon by ID"""
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}")
            response.raise_for_status()
            data = response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ResourceError(f"Pokemon {pokemon_id} not found")
            else:
                raise ResourceError(f"API error: {e.response.status_code}")
        except httpx.RequestError as e:
            raise ResourceError(f"Network error: {e}")

        return {
            "id": data["id"],
            "name": data["name"].capitalize(),
            "height": data["height"],
            "weight": data["weight"],
            "types": [t["type"]["name"] for t in data["types"]],
            "abilities": [a["ability"]["name"] for a in data["abilities"]],
            "stats": {s["stat"]["name"]: s["base_stat"] for s in data["stats"]},
            # Limit moves to first 10
            "moves": [m["move"]["name"] for m in data["moves"][:10]],
            "sprites": {k: v for k, v in data["sprites"].items() if v and isinstance(v, str)},
            "app_uri": f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
        }


@mcp.resource("pokemon://types/{type_name}")
async def get_pokemon_by_type(type_name: str) -> dict:
    """Get all Pokemon of a given type"""
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(f"https://pokeapi.co/api/v2/type/{type_name.lower()}")
            response.raise_for_status()
            data = response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ResourceError(f"Type {type_name} not found")
            else:
                raise ResourceError(f"API error: {e.response.status_code}")
        except httpx.RequestError as e:
            raise ResourceError(f"Network error: {e}")

        pokemon_list = data["pokemon"][:10]  # Limit to first 10 Pokemon
        return {
            "type": type_name.capitalize(),
            "type_id": data["id"],
            "pokemon_count": len(data["pokemon"]),
            "showing": len(pokemon_list),
            "pokemon": [p["pokemon"]["name"] for p in pokemon_list],
            "app_uri": f"https://pokeapi.co/api/v2/type/{type_name.lower()}"
        }


@mcp.resource("pokemon://starters")
async def get_starters() -> dict:
    """Get all starter Pokemon"""
    return {
        "starters": STARTERS,
        "count": len(STARTERS),
        "description": "Original starter Pokemon from the demo data"
    }


if __name__ == "__main__":
    mcp.run()
