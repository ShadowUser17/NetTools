#!/bin/bash
GO="/usr/bin/go"
CMD="./cmd"
BIN="${CMD}/$(basename ${PWD})"
MAIN="${CMD}/main.go"


if [[ -e "${BIN}" ]]; then
    rm "${BIN}" && echo "Old build is deleted."
fi

"${GO}" build -ldflags="-s -w" -o "${BIN}" "${MAIN}" && {
    echo -e "Build complete.\nUse ${BIN} to perform."
}
