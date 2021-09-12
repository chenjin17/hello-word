#@title Scan Direction (vector_scan_direction)
def vector_scan_direction(scan_params: dict, debug: bool = False):
  """Reorder pixels to correct for scan direction.

  uniform_array: array of pixel intensity[y,x]
                 typical use is U24 in dtype=np.uint32

  scan_params: dict containing
    [I/O]
    input_buffer: list containing input pixels in raster order
    input_eolf: list of [EOL, EOF] matching input_buffer
    output_buffer: list containing output pixels in time order
    output_eolf: list of [EOL, EOF] matching output_buffer

    [Parameters]
    process_chunk: max number of items to process
    start_rtol: flag indicating first line scan is right-to-left
    alternate_dir: flag indicating alternating lines should alternate scan
                   directions

    [Parameter/State]
    output_fifo: bool indicating output is being read in order (FIFO)

  Returns scan_array[y,x], dtype=np.uint32
  """
  if 'output_buffer' not in scan_params:
    scan_params['output_buffer'] = []
  if 'output_eolf' not in scan_params:
    scan_params['output_eolf'] = []

  processed = 0
  processed_target = 1
  if 'process_chunk' in scan_params:
    processed_target = scan_params['process_chunk']

  seg_length = min(len(scan_params['input_buffer']), \
                   len(scan_params['input_eolf']))
  while seg_length > 0 and processed < processed_target:
    seg_length = 0
    next_input_eol = None
    next_input_eof = None
    try:
      next_input_eol = scan_params['input_eolf'].index((True, False))
    except ValueError:
      next_input_eol = None
    try:
      next_input_eof = scan_params['input_eolf'].index((True, True))
    except ValueError:
      next_input_eof = None
    print(next_input_eol, next_input_eof)
    seg_eol = False
    seg_eof = False
    if not (next_input_eol is None):
      seg_length = next_input_eol+1
      seg_eol = True
    if not (next_input_eof is None) and \
           (seg_length == 0 or next_input_eof < seg_length):
      seg_length = next_input_eof+1
      seg_eol = True
      seg_eof = True

    if debug:
      print(f"{seg_eol} {seg_eof} Seg length {seg_length}")
    if seg_length > 0:
      # Transfer segment pixels to output buffer
      if scan_params['output_fifo']:
        scan_params['output_buffer'].extend(scan_params['input_buffer'][0:seg_length])
      else:
        scan_params['output_buffer'].extend(scan_params['input_buffer'][seg_length-1::-1])
      scan_params['output_eolf'].extend(scan_params['input_eolf'][0:seg_length])
      del scan_params['input_buffer'][0:seg_length]
      del scan_params['input_eolf'][0:seg_length]
      # Swap directions if parameter set to alternate
      if seg_eol and scan_params['alternate_dir']:
          scan_params['output_fifo'] = not scan_params['output_fifo']
      if seg_eof:
          scan_params['output_fifo'] = scan_params['start_rtol']
      if 'process_chunk' in scan_params:
        processed += 1
