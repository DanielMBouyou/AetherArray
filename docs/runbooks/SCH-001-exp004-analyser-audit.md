# SCH-001: Finish the network analyser audit, EXP-004

- ID: SCH-001
- Class: SCHOOL-BENCH
- Status: READY
- Experiment: EXP-004
- Decisions: 0004, 0006
- Last reviewed: 2026-09-26

## Why we are doing it

Five of the nine readings about the school's network analyser are incomplete: O8 was
never taken, and O1, O6, O7 and O9 are only partial. Two of them unblock purchases: decision 0006 allows the first
measurement enabling purchases, cables, adapters and antennas, only once O1 and O7 are
recorded. This visit only looks and records. It calibrates nothing and changes nothing
that has to be undone later.

## The scientific question

What exactly is this analyser, what is installed on it, and can it be calibrated at the
plane where our boards will connect? These are observations O1, O6, O7, O8 and O9 of
EXP-004, whose frequency question is already closed by decision 0004.

## What must already be true

- [ ] You have access to the school RF laboratory and permission to use the analyser.
- [ ] The analyser is the Rohde and Schwarz ZVL seen on 2026-09-20, `results/EXP-004/README.md` result 2.
- [ ] Nothing of ours is needed: no board, no cable, no calibration.

## What you need

| Item | Why it is needed |
| --- | --- |
| This runbook, printed or on a tablet | the observation sheet at the end is filled at the bench |
| A phone or camera | photographs are the evidence for O1, O7 and O8 |
| A USB memory stick, FAT32, with an empty folder `AETHERARRAY` | the export test in step 6.6 |
| The laptop with the repository, charged | O9, and a copy of every file before leaving |
| A USB A to B cable | O9; if the analyser's rear port is another type, record the type and skip O9 |
| A pen | the sheet |

## Expected duration

About 30 minutes at the bench, 45 with the optional instrument check in step 6.7.

## Files to bring or open

| File | Where it is |
| --- | --- |
| This runbook | `docs/runbooks/pdf/SCH-001-exp004-analyser-audit.pdf` |
| The readings already taken, to compare with | `results/EXP-004/README.md`, result 2 |
| The four documented instruments, for step 6.7 | `docs/hardware/measurement-bench.md`, section 2.2 |

## Files that must exist when you leave

| File | What it contains |
| --- | --- |
| `YYYY-MM-DD_EXP-004_O1_rear-label.jpg` | the whole rear label, legible |
| `YYYY-MM-DD_EXP-004_O6_source-level.jpg` | the power field showing the level set |
| `YYYY-MM-DD_EXP-004_O7_case-N.jpg`, one per case | each accessory case, open |
| `YYYY-MM-DD_EXP-004_O8_options.jpg` | the options and versions page |
| `YYYY-MM-DD_EXP-004_O9_usb.png` | the laptop's device list after connecting |
| `YYYY-MM-DD_EXP-004_export-test.s1p` | the export test, if it could be taken |
| `YYYY-MM-DD_EXP-004_sheet.jpg` | the filled observation sheet |

## STOP / DO NOT CONTINUE

Stop, record why on the sheet, and leave the instrument as you found it, if:

- **the analyser is not a ZVL, or its rear label cannot be read.** Record what you see.
  Do not infer the model from the front panel: result 2 already did that, and it is
  exactly what this visit replaces.
- **someone else's setup or calibration is loaded and you have no permission to touch
  it.** Do not preset, and do not save over their files.
- **a reading would need a user calibration, a change of reference plane, or a cable of
  ours.** None of this visit needs them; they belong to a later runbook.
- **a limit can only be reached through service or factory settings.** Record the limit
  the normal menus accept instead.
- **the laptop asks to install a driver from an unknown source.** Do not install it;
  record the device name and skip the rest of O9.

## Procedure

### 1. Open the application or instrument

1. Find the analyser and photograph the front panel as found.
2. If it is off, switch it on and wait until the measurement screen appears.
3. Do not preset it yet.

### 2. Load the project or set up the connection

1. There is no project to load.
2. If a setup is on screen, ask whether it may be changed. If allowed, save it under a
   new name, for example `AETHERARRAY_BEFORE`, so it can be restored in step 10.
3. Insert the USB stick.

### 3. Settings and parameters

| Reading | What to do | Value to use | Source |
| --- | --- | --- | --- |
| O6, source level | set the output power field | $-10$ dBm | `docs/hardware/measurement-bench.md` section 5 |
| O6, range | try the lowest and the highest value the field accepts | whatever it accepts | EXP-004 O6 |
| Export test sweep | start, stop and points | 2.30 to 2.60 GHz, 121 points | the EXP-011 grid |

> [!NOTE]
> For conducted work, 0 dBm into the board with about 4 dB of chain loss would put the
> detector near the top of its range, so $-10$ dBm is the proposed default. It is far below the radiated ceiling EXP-004 derived from the regulation:
>
> ```math
> P_{\mathrm{src}} \le P_{\mathrm{EIRP}} - G_{\mathrm{probe}} = 10\ \mathrm{dBm} - 2\ \mathrm{dBi} = 8\ \mathrm{dBm}
> ```
>
> and this analyser cannot exceed 0 dBm anyway. If $-10$ dBm is not accepted, use the
> nearest accepted value and record it: O6 asks for the level actually used.

### 4. What not to change

- No factory or service settings, no firmware update, no option or licence change.
- No user calibration, and no file deleted or overwritten on the instrument.
- Leave the port savers on the test ports if they are fitted: they protect connectors
  that cost more than this project.

### 5. Checks before launching

- [ ] The analyser sees the USB stick: a file dialog lists it.
- [ ] Nothing is connected to either test port except port savers.
- [ ] A test photograph of small print is sharp when zoomed.

### 6. Launch

Take the readings in this order, and write each one on the sheet as you go.

1. **O1.** Photograph the whole rear label. Copy every field exactly, including the
   model, the material or order number and the serial number.
2. **O8.** Open the instrument's version and options page. On this family it is reached
   from the setup key, under an entry named Info, System Info or Versions and Options.
   Photograph it, copy every option code verbatim, and write down the menu path you used
   and the firmware version.
3. **O6.** Set the output power to the value in step 3, photograph the field, then try
   the lowest and highest accepted values and record them.
4. **O7.** Open every accessory case near the analyser. For each item record the printed
   model or part number, what it is (open, short, load, through, adapter, cable, torque
   wrench), and its connector type and sex: N, 3.5 mm or SMA, male or female.
   Photograph each case.
5. **O9.** Record every port on the rear panel as labelled: USB and its type, LAN, GPIB.
   Connect the USB cable from the analyser's device port to the laptop, open the device
   list, and record any new device, with its hardware identifier.
6. **Export test.** With nothing on port 1, display S11 over the sweep in step 3 and save
   the trace data as a Touchstone `.s1p` file to the USB stick. This is not a measurement
   of anything: it proves that data leave the instrument in a form `rfkit` can read.
7. **Optional.** Look for the four instruments listed in
   `docs/hardware/measurement-bench.md` section 2.2 and record each as present, with its
   model plate, or not seen.

### 7. What success looks like

- A full model string and a serial number for O1.
- A list of option codes for O8, even if it is short.
- For O7, either an inventory of the cases or the words "no case found". **No
  calibration kit is a valid result**, not a failure: it is the answer decision 0006
  needs.
- For O9, either a device name with its identifier, or "no device appeared".
- One `.s1p` file on the stick whose first lines start with `!` or `#`.

### 8. Export and save

1. Save a screenshot of the options page to the stick, if the analyser can print to file.
2. Copy everything from the stick to the laptop.
3. Photograph the filled sheet.

### 9. File names and destination

| File | Name | Destination in AetherArray |
| --- | --- | --- |
| Every photograph and screenshot | `YYYY-MM-DD_EXP-004_<reading>_<what>.<ext>` | `results/EXP-004/raw/YYYY-MM-DD/` |
| The export test | `YYYY-MM-DD_EXP-004_export-test.s1p` | same |
| The sheet | `YYYY-MM-DD_EXP-004_sheet.jpg` | same |

`raw/` stays on the laptop and is not committed; `results/README.md` explains why.

### 10. Final checklist before leaving

- [ ] The analyser is back as you found it: the saved setup recalled, or preset only if that was its state.
- [ ] The source level is no higher than you found it.
- [ ] The USB stick and cable are removed, and the cases are closed and put back.
- [ ] Every row of the sheet is filled, or marked "not obtainable" with the reason.
- [ ] The photographs are legible when zoomed.
- [ ] Every file is on both the stick and the laptop.

## Evidence to bring back

- The rear label photograph, O1.
- The options page photograph or screenshot, and its verbatim transcription, O8.
- The power field photograph and the accepted range, O6.
- One photograph per accessory case, and the item list, O7.
- The rear panel port list and the device list screenshot, O9.
- The `.s1p` export test file.
- The filled observation sheet.

## Back at home

1. Put the files in `results/EXP-004/raw/YYYY-MM-DD/`, and record each one with its
   checksum in `results/EXP-004/SOURCE.md`: `sha256sum results/EXP-004/raw/YYYY-MM-DD/*`.
2. Check that the export test reads, from the repository root:

   ```
   cd tools
   python -c "import rfkit; print(rfkit.load_touchstone('../results/EXP-004/raw/YYYY-MM-DD/YYYY-MM-DD_EXP-004_export-test.s1p', source='vna').describe())"
   ```
3. Fill rows O1, O6, O7, O8 and O9 of `results/EXP-004/README.md`, each checked against
   the data sheet of the model O1 names, and update bibliography entry T1.
4. **If O1 names a model specified below 2.44 GHz, decision 0004 reopens** by its first
   condition. Stop there.
5. Otherwise, with O1 and O7 recorded, decision 0006 allows the interconnect and antenna
   purchases, sized by what O7 found. EXP-004 closes when all nine readings are recorded.
6. Mark SCH-001 as done in `docs/runbooks/register.md`.

## Observation sheet

| Reading | Value | Photo or file |
| --- | --- | --- |
| O1 model, material or order number, serial | | |
| O6 level used, accepted minimum and maximum | | |
| O7 cases and items, connector types | | |
| O8 option codes, firmware, menu path | | |
| O9 rear ports, device seen on the laptop | | |
| Export test saved | yes or no | |
| Optional: N9923A, 8714C, N9000A, 8562A | present or not seen, each | |
