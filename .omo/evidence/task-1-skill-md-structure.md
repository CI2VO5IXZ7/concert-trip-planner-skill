## Task 1 Verification Evidence

- File: `/home/momentg/Project/tezhongbing/SKILL.md`
- `grep -c "references/" SKILL.md` → `5`
- `grep -c "Must Have\|Must NOT Have" SKILL.md` → `2`
- `grep -c "concert\|演唱会\|特种兵" SKILL.md` → `10`

Result: all required counts are `>= 1`.
