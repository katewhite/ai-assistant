#!/usr/bin/env python3
"""
Script to inspect Granola cache for speaker information in transcripts
"""

import json
from pathlib import Path
from config import GRANOLA_CACHE_PATH

def load_granola_cache():
    """Load and parse the Granola cache-v3.json file."""
    if not GRANOLA_CACHE_PATH.exists():
        raise FileNotFoundError(f"Granola cache not found at: {GRANOLA_CACHE_PATH}")

    with open(GRANOLA_CACHE_PATH, "r") as f:
        top = json.load(f)

        # Double-decode the embedded JSON string if necessary
        if isinstance(top.get("cache"), str):
            top["cache"] = json.loads(top["cache"])

        return top

def inspect_transcript_for_speakers(doc_id, cache_data):
    """Inspect a specific document's transcript for speaker information."""
    state = cache_data.get("cache", {}).get("state", {})
    documents = state.get("documents", {})
    transcripts = state.get("transcripts", {})
    
    if doc_id not in documents:
        print(f"Document {doc_id} not found")
        return
    
    if doc_id not in transcripts:
        print(f"Transcript for {doc_id} not found")
        return
    
    doc = documents[doc_id]
    transcript_data = transcripts[doc_id]
    
    print(f"\n{'='*80}")
    print(f"Document: {doc.get('title', 'Untitled')}")
    print(f"Document ID: {doc_id}")
    print(f"{'='*80}\n")
    
    # Check document structure
    print("DOCUMENT STRUCTURE:")
    print(f"  Document keys: {list(doc.keys())}")
    if "people" in doc:
        print(f"  People structure: {doc['people']}")
    print()
    
    # Check transcript structure
    print("TRANSCRIPT STRUCTURE:")
    if isinstance(transcript_data, list):
        print(f"  Transcript is a list with {len(transcript_data)} segments")
        if transcript_data:
            print(f"  First segment keys: {list(transcript_data[0].keys())}")
            print(f"  First segment full data: {json.dumps(transcript_data[0], indent=2)}")
            
            # Check first 5 segments
            print(f"\n  First 5 segments:")
            for i, segment in enumerate(transcript_data[:5]):
                print(f"    Segment {i}: {json.dumps(segment, indent=4)}")
    elif isinstance(transcript_data, dict):
        print(f"  Transcript is a dict with keys: {list(transcript_data.keys())}")
        print(f"  Full transcript data: {json.dumps(transcript_data, indent=2)}")
    else:
        print(f"  Transcript type: {type(transcript_data)}")
    print()
    
    # Check state for speaker-related structures
    print("STATE STRUCTURE:")
    print(f"  All state keys: {list(state.keys())}")
    
    # Look for speaker-related keys
    speaker_keys = [k for k in state.keys() if "speaker" in k.lower()]
    if speaker_keys:
        print(f"  Speaker-related keys found: {speaker_keys}")
        for key in speaker_keys:
            data = state.get(key, {})
            if doc_id in data:
                print(f"    {key} for this doc: {json.dumps(data[doc_id], indent=4)}")
    else:
        print(f"  No speaker-related keys found in state")
    
    # Look for transcript-related keys
    transcript_keys = [k for k in state.keys() if "transcript" in k.lower()]
    print(f"  Transcript-related keys: {transcript_keys}")
    for key in transcript_keys:
        data = state.get(key, {})
        if doc_id in data:
            print(f"    {key} for this doc: {json.dumps(data[doc_id], indent=4)}")
    print()
    
    # Check for any segment-level speaker info
    print("SEGMENT-LEVEL SPEAKER CHECK:")
    if isinstance(transcript_data, list):
        for i, segment in enumerate(transcript_data[:10]):  # Check first 10
            if isinstance(segment, dict):
                # Check all keys for anything that might indicate speaker
                all_keys = list(segment.keys())
                potential_speaker_keys = [k for k in all_keys if any(term in k.lower() for term in ['speaker', 'user', 'person', 'attendee', 'name', 'label'])]
                if potential_speaker_keys:
                    print(f"  Segment {i} has potential speaker keys: {potential_speaker_keys}")
                    for key in potential_speaker_keys:
                        print(f"    {key}: {segment[key]}")
    print()

if __name__ == "__main__":
    # Document ID from the call we've been working with
    doc_id = "572d2e5c-8460-4b43-9fab-09ebf062cd1c"
    
    print("Loading Granola cache...")
    cache_data = load_granola_cache()
    
    print(f"Inspecting document: {doc_id}")
    inspect_transcript_for_speakers(doc_id, cache_data)
