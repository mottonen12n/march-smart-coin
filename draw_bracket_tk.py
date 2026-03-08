"""Simple Tkinter app to draw a 64-team single-elimination bracket.

Run: python draw_bracket_tk.py

Clicking a team currently does nothing; this is a visual generator.
"""
import tkinter as tk
from tkinter import ttk

def generate_default_teams(n=64):
    return [f"Team {i+1}" for i in range(n)]

def generate_placeholder_winners(n=64):
    # generate placeholder winners for testing
    winners = []
    # round 1 winners (32)
    for i in range(32):
        winners.append(f"Round 1 Winner {i+1}")
    # round 2 winners (16)
    for i in range(16):
        winners.append(f"Round 2 Winner {i+1}")
    # round 3 winners (8)
    for i in range(8):
        winners.append(f"Round 3 Winner {i+1}")
    # round 4 winners (4)
    for i in range(4):
        winners.append(f"Round 4 Winner {i+1}")
    # round 5 winners (2)
    for i in range(2):
        winners.append(f"Round 5 Winner {i+1}")
    # champion
    winners.append("Champion")
    return winners


class BracketCanvas(tk.Frame):
    def __init__(self, master, teams, winners, column_width=140, v_spacing=24, left_margin=20, top_margin=20, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.teams = teams
        self.num_teams = len(teams)
        self.rounds = 0
        self.winners = winners
        #self.winners = ["Team 1", "Team 3", "Team 5", "Team 7", "Team 9", "Team 11", "Team 13", "Team 15", "Team 17", "Team 19", "Team 21", "Team 23", "Team 25", "Team 27", "Team 29", "Team 31", "Team 33", "Team 35", "Team 37", "Team 39", "Team 41", "Team 43", "Team 45", "Team 47", "Team 49", "Team 51", "Team 53", "Team 55", "Team 57", "Team 59", "Team 61", "Team 63", "Team 1", "Team 5", "Team 9", "Team 13", "Team 17", "Team 21", "Team 25", "Team 29", "Team 33", "Team 37", "Team 41", "Team 45", "Team 49", "Team 53", "Team 57", "Team 61", "Team 1", "Team 9", "Team 17", "Team 25", "Team 33", "Team 41", "Team 49", "Team 57", "Team 1", "Team 17", "Team 33", "Team 49", "Team 1", "Team 33", "Team 1"] # placeholder winners for testing
        t = self.num_teams
        while t > 1:
            t //= 2
            self.rounds += 1

        self.column_width = column_width
        self.v_spacing = v_spacing
        self.left_margin = left_margin
        self.top_margin = top_margin

        # make room for left and right side columns and a center area for semis/final
        base_canvas_width = left_margin + (self.rounds + 1) * column_width + left_margin + 120
        # increase total width by 30% then further increase by 25%
        canvas_width = int(base_canvas_width * 1.5)
        canvas_height = top_margin + max(600, int(self.num_teams * v_spacing)) + 120

        self.canvas = tk.Canvas(self, width=canvas_width, height=800, scrollregion=(0, 0, canvas_width, canvas_height), bg="#ffffff")
        # cache total drawing width for consistent layout calculations
        self.total_width = canvas_width
        vbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=vbar.set)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        vbar.grid(row=0, column=1, sticky="ns")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.positions = {}  # key: (round, index) -> y
        self._compute_positions()
        self._draw_bracket()

    def _compute_positions(self):
        # Place teams into four quadrants: 0-15 TL, 16-31 TR, 32-47 BL, 48-63 BR
        quad_count = self.num_teams // 4  # 16
        quad_height = (quad_count - 1) * self.v_spacing
        gap_between = 40
        top_start = self.top_margin
        bottom_start = top_start + quad_height + gap_between

        for i in range(self.num_teams):
            if i < quad_count:  # TL
                y = top_start + (i % quad_count) * self.v_spacing
            elif i < quad_count * 2:  # TR
                y = top_start + (i - quad_count) * self.v_spacing
            elif i < quad_count * 3:  # BL
                y = bottom_start + (i - quad_count * 2) * self.v_spacing
            else:  # BR
                y = bottom_start + (i - quad_count * 3) * self.v_spacing
            self.positions[(0, i)] = y

        # Subsequent rounds: average of two children (works because indices are grouped by quadrant)
        teams_in_round = self.num_teams
        for r in range(1, self.rounds + 1):
            teams_in_round //= 2
            for i in range(teams_in_round):
                child_a = self.positions[(r - 1, i * 2)]
                child_b = self.positions[(r - 1, i * 2 + 1)]
                self.positions[(r, i)] = (child_a + child_b) / 2

        # place round-5 (semifinal) nodes halfway between their round-4 children and the champion
        if self.rounds >= 6:
            champ_y = self.positions[(self.rounds, 0)]
            items_r5 = self.num_teams // (2 ** 5)
            for i in range(items_r5):
                child_a = self.positions[(4, i * 2)]
                child_b = self.positions[(4, i * 2 + 1)]
                child_avg = (child_a + child_b) / 2
                self.positions[(5, i)] = (child_avg + champ_y) / 2

        # cache some layout helpers
        self.center_x = int(self.total_width // 2)

    def _x_for_round(self, r):
        return self.left_margin + r * self.column_width

    def _x_for_position(self, r, i):
        # determine representative leaf index under this node (use midpoint of leaf range)
        if r == 0:
            leaf0 = i
        else:
            span = 2 ** r
            leaf0 = i * span + span // 2

        quad_size = self.num_teams // 4

        # x coordinates for left and right columns for each round
        left_xs = [self.left_margin + rr * self.column_width for rr in range(0, min(self.rounds, 6))]
        canvas_w = self.total_width
        right_xs = [canvas_w - (self.left_margin + rr * self.column_width) for rr in range(0, min(self.rounds, 6))]

        # quadrant detection
        if leaf0 < quad_size:
            quad = 0  # TL
        elif leaf0 < quad_size * 2:
            quad = 1  # TR
        elif leaf0 < quad_size * 3:
            quad = 2  # BL
        else:
            quad = 3  # BR

        # internal rounds (r <= 4) stay on left or right side
        if r <= 4:
            idx = r if r < len(left_xs) else len(left_xs) - 1
            base = left_xs[idx] if quad in (0, 2) else right_xs[idx]
            # move round 4 slightly toward center to avoid overlap with semis
            if r == 4:
                # move round-4 nodes halfway toward center but don't cross it
                if base < self.center_x:
                    # left side -> move right
                    new_x = int(base + (self.center_x - base) * 0.5)
                    return min(new_x, self.center_x - 40)
                else:
                    # right side -> move left
                    new_x = int(base - (base - self.center_x) * 0.5)
                    return max(new_x, self.center_x + 40)
            return base

        # r == 5 -> semifinal nodes: align vertically with champion (same center x)
        if r == 5:
            return self.center_x

        # champion
        return self.center_x

    def _draw_bracket(self):
        # draw team text for round 0
        text_pad = 4
        # store text bounding boxes so connectors can start at text edges
        self.text_bbox = {}
        self.canvas.update_idletasks()
        for i, name in enumerate(self.teams):
            x = self._x_for_position(0, i)
            y = self.positions[(0, i)]
            anchor = "w" if x < (self.center_x) else "e"
            tid = self.canvas.create_text(x, y, anchor=anchor, text=name, font=("Arial", 10))
            self.canvas.update_idletasks()
            bbox = self.canvas.bbox(tid)
            self.text_bbox[(0, i)] = bbox

        # draw placeholders for later rounds and connectors
        for r in range(1, self.rounds + 1):
            items = self.num_teams // (2 ** r)
            for i in range(items):
                x = self._x_for_position(r, i)
                y = self.positions[(r, i)]
                # placeholder text
                match r:
                    case 1:
                        txt = self.winners[i]
                    case 2:
                        txt = self.winners[i + 32]
                    case 3:
                        txt = self.winners[i + 48]
                    case 4:
                        txt = self.winners[i + 56]
                    case 5:
                        txt = self.winners[i + 60]
                    case 6:
                        txt = self.winners[62]
                anchor = "w" if x < (self.center_x) else "e"
                tid = self.canvas.create_text(x, y, anchor=anchor, text=txt, font=("Arial", 10, "italic"))
                self.canvas.update_idletasks()
                bbox = self.canvas.bbox(tid)
                self.text_bbox[(r, i)] = bbox

        # draw connecting lines from children to parent
        for r in range(1, self.rounds + 1):
            for i in range(self.num_teams // (2 ** r)):
                parent_x = self._x_for_position(r, i)
                y_parent = self.positions[(r, i)]
                child_a_idx = i * 2
                child_b_idx = i * 2 + 1
                child_a_x = self._x_for_position(r - 1, child_a_idx)
                child_b_x = self._x_for_position(r - 1, child_b_idx)
                y_child_a = self.positions[(r - 1, child_a_idx)]
                y_child_b = self.positions[(r - 1, child_b_idx)]

                offset = 40
                # choose outward offsets depending on side
                # use child text bbox edges as connector start points
                cb_a = self.text_bbox.get((r - 1, child_a_idx))
                cb_b = self.text_bbox.get((r - 1, child_b_idx))

                # Special handling for final connectors: connect semis to champion using text centers and top/bottom edges
                if r == self.rounds:
                    pb = self.text_bbox.get((r, i))
                    # champion bbox center x
                    if pb:
                        pb_cx = (pb[0] + pb[2]) / 2
                    else:
                        pb_cx = parent_x

                    # top semifinal (child_a) start at its horizontal center and bottom y
                    if cb_a:
                        sa_x = (cb_a[0] + cb_a[2]) / 2
                        sa_y = cb_a[3]
                    else:
                        sa_x = child_a_x
                        sa_y = y_child_a

                    # bottom semifinal (child_b) start at its horizontal center and top y
                    if cb_b:
                        sb_x = (cb_b[0] + cb_b[2]) / 2
                        sb_y = cb_b[1]
                    else:
                        sb_x = child_b_x
                        sb_y = y_child_b

                    # champion top and bottom y (fallback to parent y if missing)
                    if pb:
                        champ_top = pb[1]
                        champ_bottom = pb[3]
                    else:
                        champ_top = y_parent - 6
                        champ_bottom = y_parent + 6

                    self.canvas.create_line(sa_x, sa_y, pb_cx, champ_top, width=1)
                    self.canvas.create_line(sb_x, sb_y, pb_cx, champ_bottom, width=1)
                elif r == 5:
                    # connectors from round-4 winners to round-5 nodes
                    # For the top semifinal (i==0) both connectors should start at the bottom-center
                    # of their round-4 text and connect to the top-center of the round-5 text.
                    # For the bottom semifinal both connectors start at the top-center and connect
                    # to the bottom-center of the round-5 text.
                    rb = self.text_bbox.get((r, i))
                    # round-5 target center x and its top/bottom y
                    if rb:
                        rb_cx = (rb[0] + rb[2]) / 2
                        rb_top = rb[1]
                        rb_bottom = rb[3]
                    else:
                        rb_cx = parent_x
                        rb_top = y_parent - 6
                        rb_bottom = y_parent + 6

                    top_semif = (i == 0)

                    # compute starts for both children
                    if cb_a:
                        a_cx = (cb_a[0] + cb_a[2]) / 2
                        a_top = cb_a[1]
                        a_bottom = cb_a[3]
                    else:
                        a_cx = child_a_x
                        a_top = y_child_a
                        a_bottom = y_child_a

                    if cb_b:
                        b_cx = (cb_b[0] + cb_b[2]) / 2
                        b_top = cb_b[1]
                        b_bottom = cb_b[3]
                    else:
                        b_cx = child_b_x
                        b_top = y_child_b
                        b_bottom = y_child_b

                    if top_semif:
                        # both start at bottom-center -> connect to rb_top
                        self.canvas.create_line(a_cx, a_bottom, rb_cx, rb_top, width=1)
                        self.canvas.create_line(b_cx, b_bottom, rb_cx, rb_top, width=1)
                    else:
                        # both start at top-center -> connect to rb_bottom
                        self.canvas.create_line(a_cx, a_top, rb_cx, rb_bottom, width=1)
                        self.canvas.create_line(b_cx, b_top, rb_cx, rb_bottom, width=1)
                else:
                    # fallback to using text edge starts or offset if bbox missing
                    if cb_a:
                        start_a = cb_a[2] + 6 if (cb_a[0] + cb_a[2]) / 2 < self.center_x else cb_a[0] - 6
                    else:
                        start_a = child_a_x + offset if child_a_x < parent_x else child_a_x - offset

                    if cb_b:
                        start_b = cb_b[2] + 6 if (cb_b[0] + cb_b[2]) / 2 < self.center_x else cb_b[0] - 6
                    else:
                        start_b = child_b_x + offset if child_b_x < parent_x else child_b_x - offset

                    xp = parent_x - 10 if parent_x > child_a_x else parent_x + 10

                    self.canvas.create_line(start_a, y_child_a, xp, y_parent, width=1)
                    self.canvas.create_line(start_b, y_child_b, xp, y_parent, width=1)

    def close(self):
        self.master.destroy()


def main(teams=None, winners=None):
    if teams is None:
        teams = generate_default_teams(64)
    if winners is None:
        winners = generate_placeholder_winners(64)

    root = tk.Tk()
    root.title("Smart Coin Generated Bracket")

    frame = BracketCanvas(root, teams, winners)
    frame.pack(fill="both", expand=True)

    # set window geometry to match drawing width (height leaves room for controls)
    root.update_idletasks()
    try:
        root.geometry(f"{frame.total_width}x820")
    except Exception:
        pass

    info = tk.Label(root, text="Scroll vertically to view full bracket. Close window to exit.")
    info.pack(side="bottom", fill="x")

    root.mainloop()

    


if __name__ == "__main__":
    main()
