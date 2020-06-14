from .._yosys import *
from . import rtlil


__all__ = ["YosysError", "convert", "convert_fragment"]


def _convert_rtlil_text(rtlil_text, black_boxes, *, src_loc_at=0):
    if black_boxes is not None:
        if not isinstance(black_boxes, dict):
            raise TypeError("CXXRTL black boxes must be a dictionary, not {!r}"
                            .format(black_boxes))
        for box_name, box_source in black_boxes.items():
            if not isinstance(box_name, str):
                raise TypeError("CXXRTL black box name must be a string, not {!r}"
                                .format(box_name))
            if not isinstance(box_source, str):
                raise TypeError("CXXRTL black box source code must be a string, not {!r}"
                                .format(box_source))

     # FIXME: update this requirement once Yosys updates its node version
    yosys = find_yosys(lambda ver: ver >= (0, 9))

    script = []
    if black_boxes is not None:
        for box_name, box_source in black_boxes.items():
            script.append("read_ilang <<rtlil\n{}\nrtlil".format(box_source))
    script.append("read_ilang <<rtlil\n{}\nrtlil".format(rtlil_text))
    script.append("delete w:$verilog_initial_trigger")
    script.append("write_cxxrtl")

    return yosys.run(["-q", "-"], "\n".join(script), src_loc_at=1 + src_loc_at)


def convert_fragment(*args, black_boxes=None, **kwargs):
    rtlil_text, name_map = rtlil.convert_fragment(*args, **kwargs)
    return _convert_rtlil_text(rtlil_text, black_boxes, src_loc_at=1), name_map


def convert(*args, black_boxes=None, **kwargs):
    rtlil_text = rtlil.convert(*args, **kwargs)
    return _convert_rtlil_text(rtlil_text, black_boxes, src_loc_at=1)
