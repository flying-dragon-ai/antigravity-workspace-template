# vhs tape file — RepoBrain README hero demo
#
# Prerequisites:
#   brew install vhs
#
# Build:
#   vhs docs/assets/demo.tape
#
# Outputs: docs/assets/demo.gif (≈ 30s, ≤ 5MB target)

Output docs/assets/demo.gif

Set FontSize 18
Set FontFamily "JetBrains Mono"
Set Width 1280
Set Height 720
Set Padding 40
Set Theme "Catppuccin Mocha"
Set TypingSpeed 55ms
Set PlaybackSpeed 1.0

# Use the demo mock so the recording doesn't depend on a live LLM call
Hide
Type "alias rb-ask='bash docs/assets/demo-mock.sh'"
Enter
Type "clear"
Enter
Show

Sleep 800ms
Type "rb-ask "
Sleep 200ms
Type `'How does the multi-agent cluster work?'`
Sleep 500ms
Enter

# Mock script self-paces its output (sleeps + colorized lines)
Sleep 8s

# Tail: a second, structural question to show graph enrichment
Type "rb-ask "
Sleep 200ms
Type `'Who calls refresh_pipeline?'`
Sleep 500ms
Enter
Sleep 6s

Sleep 1.5s
