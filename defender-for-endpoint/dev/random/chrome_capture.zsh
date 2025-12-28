#!/bin/zsh

# ==============================================================================
# SCRIPT METADATA
# ==============================================================================
# Script Name:  chrome_capture.zsh
# Author:       Adair John Collins (@adairjcollins)
# Description:  Automates evidence acquisition by capturing:
#               1. Raw HTTP Response (Curl)
#               2. Rendered DOM (Headless Chrome)
#               3. Full Page Screenshot (Headless Chrome)
# Version:      2.0
# ==============================================================================

# --- DEFAULT CONFIGURATION ---
# You can override these via command-line flags.
DEFAULT_CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
DEFAULT_OUT_DIR="results"
DEFAULT_UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Initialize variables
CHROME_BIN="$DEFAULT_CHROME"
OUTPUT_DIR="$DEFAULT_OUT_DIR"
USER_AGENT="$DEFAULT_UA"
INPUT_FILE=""

# --- COLORS ---
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

usage() {
    echo -e "${BLUE}Usage:${NC} $0 -f <input_file> [options]"
    echo -e "\n${YELLOW}Description:${NC}"
    echo -e "  Automates the collection of raw source, rendered DOM, and screenshots"
    echo -e "  using Curl and Headless Chrome."
    echo -e "\n${YELLOW}Required Arguments:${NC}"
    echo -e "  -f <file>    Path to the text file containing the list of URLs/IPs."
    echo -e "\n${YELLOW}Optional Arguments:${NC}"
    echo -e "  -b <path>    Path to Chrome/Chromium binary."
    echo -e "               ${BLUE}Default:${NC} $DEFAULT_CHROME"
    echo -e "  -o <path>    Directory to save results."
    echo -e "               ${BLUE}Default:${NC} $DEFAULT_OUT_DIR"
    echo -e "  -u <string>  User-Agent string to use for both Curl and Chrome."
    echo -e "               ${BLUE}Default:${NC} macOS Chrome 120"
    echo -e "  -h           Show this help message."
    echo -e "\n${YELLOW}Example:${NC}"
    echo -e "  $0 -f targets.txt -o my_scan_results"
    echo -e "  $0 -f ips.txt -b /usr/bin/chromium"
    exit 1
}

validate_inputs() {
    # 1. Validate Input File
    if [[ -z "$INPUT_FILE" ]]; then
        echo -e "${RED}[!] Error: No input file specified.${NC}"
        usage
    fi

    if [[ ! -f "$INPUT_FILE" ]]; then
        echo -e "${RED}[!] Error: Input file not found at: $INPUT_FILE${NC}"
        exit 1
    fi

    # 2. Validate Chrome Binary
    if [[ ! -f "$CHROME_BIN" ]]; then
        echo -e "${RED}[!] Error: Chrome binary not found at: $CHROME_BIN${NC}"
        echo "    Please install Chrome or specify the correct path using -b"
        exit 1
    fi

    # 3. Create Output Directory if needed
    if [[ ! -d "$OUTPUT_DIR" ]]; then
        echo -e "${BLUE}[*] Creating output directory: $OUTPUT_DIR${NC}"
        mkdir -p "$OUTPUT_DIR"
        if [[ $? -ne 0 ]]; then
             echo -e "${RED}[!] Error: Could not create directory $OUTPUT_DIR${NC}"
             exit 1
        fi
    fi
}

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

# Parse Command Line Options
if [[ $# -eq 0 ]]; then
    usage
fi

while getopts ":f:b:o:u:h" opt; do
  case ${opt} in
    f)
      INPUT_FILE="$OPTARG"
      ;;
    b)
      CHROME_BIN="$OPTARG"
      ;;
    o)
      OUTPUT_DIR="$OPTARG"
      ;;
    u)
      USER_AGENT="$OPTARG"
      ;;
    h)
      usage
      ;;
    \?)
      echo -e "${RED}Invalid Option: -$OPTARG${NC}" 1>&2
      usage
      ;;
    :)
      echo -e "${RED}Option -$OPTARG requires an argument.${NC}" 1>&2
      usage
      ;;
  esac
done

# Run Validation
validate_inputs

# Start Loop
echo -e "${BLUE}[*] Starting capture flow...${NC}"
echo -e "${BLUE}[*] User-Agent:${NC} $USER_AGENT"
echo -e "${BLUE}[*] Output Dir:${NC} $OUTPUT_DIR"

while IFS= read -r target || [[ -n "$target" ]]; do
    # Cleanup target string
    target=$(echo "$target" | xargs)
    
    # Skip empty lines
    if [[ -z "$target" ]]; then continue; fi
    
    # Ensure protocol
    if [[ ! "$target" =~ ^http ]]; then
        full_url="http://$target"
    else
        full_url="$target"
    fi

    # Generate clean folder name
    folder_name=$(echo "$target" | sed 's|http[s]*://||g' | tr ':' '_')
    target_path="$OUTPUT_DIR/$folder_name"

    echo -e "${YELLOW}---------------------------------------------------${NC}"
    echo -e "Target: $full_url"
    echo -e "Saving to: $target_path"

    mkdir -p "$target_path"

    # --- STEP 1: RAW SOURCE (CURL) ---
    echo -e "  > Downloading Raw Source..."
    if curl -s -L -k -A "$USER_AGENT" --max-time 10 "$full_url" -o "$target_path/raw_source.html"; then
        echo -e "${GREEN}    [OK] Saved raw_source.html${NC}"
    else
        echo -e "${RED}    [FAIL] Curl connection failed${NC}"
        echo "Connection Failed" > "$target_path/error.log"
    fi

    # --- STEP 2: RENDERED DOM (CHROME) ---
    echo -e "  > Dumping Rendered DOM..."
    "$CHROME_BIN" --headless --disable-gpu --user-agent="$USER_AGENT" --dump-dom "$full_url" > "$target_path/rendered_dom.html" 2>/dev/null
    
    if [[ -s "$target_path/rendered_dom.html" ]]; then
         echo -e "${GREEN}    [OK] Saved rendered_dom.html${NC}"
    else
         echo -e "${RED}    [FAIL] Empty DOM or Chrome crash${NC}"
    fi

    # --- STEP 3: SCREENSHOT (CHROME) ---
    echo -e "  > Taking Screenshot..."
    "$CHROME_BIN" --headless --disable-gpu --user-agent="$USER_AGENT" --screenshot="$target_path/screenshot.png" --window-size=1280,1024 "$full_url" 2>/dev/null

    if [[ -f "$target_path/screenshot.png" ]]; then
         echo -e "${GREEN}    [OK] Saved screenshot.png${NC}"
    else
         echo -e "${RED}    [FAIL] Screenshot failed${NC}"
    fi

done < "$INPUT_FILE"

echo -e "${YELLOW}---------------------------------------------------${NC}"
echo -e "${GREEN}[DONE] All targets processed.${NC}"
