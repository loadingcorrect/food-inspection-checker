
import os
import sys
import json
from pathlib import Path

# Add src to path
current_dir = Path(__file__).resolve().parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

# Mock configuration
config = {
    "RAGFLOW_API_URL": "http://114.55.65.26:80/api/v1/retrieval",
    "RAGFLOW_API_KEY": "ragflow-M2M1YjMzYTM5ZTFhMTFefa940242ac120006",
    "RAGFLOW_KB_ID": "67414df6330911efb4480242ac120006", # Default KB
    "RAGFLOW_KB_ID_GB": "67414df6330911efb4480242ac120006" # GB KB
}

# Try loading real config
config_path = current_dir / "config.local.json"
if config_path.exists():
    with open(config_path, "r", encoding="utf-8") as f:
        local_conf = json.load(f)
        config.update(local_conf)

print(f"Using Config: {json.dumps(config, indent=2)}")

try:
    from ragflow_client import get_ragflow_client
    from ragflow_verifier import verify_inspection_compliance
    print("\n[1] Testing RAGFlow Client Initialization...")
    client = get_ragflow_client(config)
    if client:
        print("Client initialized successfully.")
    else:
        print("Failed to initialize client.")
        sys.exit(1)

    food_name = "黄瓜"
    print(f"\n[2] Testing Query for '{food_name}'...")
    results = client.query_inspection_items(food_name)
    print(f"Query returned {len(results)} chunks.")
    for i, chunk in enumerate(results[:3]):
        print(f"--- Chunk {i+1} ---")
        print(f"Score: {chunk.get('score')}")
        content = chunk.get('content', '')[:100].replace('\n', ' ')
        print(f"Content: {content}...")

    print(f"\n[3] Testing Compliance Verification Logic...")
    # Mock report items
    mock_items = [
        {"item": "毒死蜱", "method": "GB 23200.113-2018", "value": "0.01"},
        {"item": "腐霉利", "method": "GB 23200.8-2016", "value": "0.02"}
    ]
    report_gb_codes = ["GB 2763-2021"]
    
    verification = verify_inspection_compliance(food_name, mock_items, report_gb_codes, config)
    print("\nVerification Result:")
    print(json.dumps(verification, ensure_ascii=False, indent=2))

except Exception as e:
    print(f"\n[ERROR] Exception occurred: {e}")
    import traceback
    traceback.print_exc()
