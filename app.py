import streamlit as st
import time
import random
from typing import List, Tuple, Dict

# Page config
st.set_page_config(page_title="Cache Memory Visualizer", layout="wide", initial_sidebar_state="collapsed")

# Initialize session state
if 'simulator' not in st.session_state:
    st.session_state.simulator = None
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0
if 'sequence' not in st.session_state:
    st.session_state.sequence = []
if 'running' not in st.session_state:
    st.session_state.running = False
if 'animation_mode' not in st.session_state:
    st.session_state.animation_mode = "Auto-Run"
if 'step_processed' not in st.session_state:
    st.session_state.step_processed = False
if 'theme' not in st.session_state:
    st.session_state.theme = "Light"
if 'sequence_input' not in st.session_state:
    st.session_state.sequence_input = "1,2,3,4,1,2,5,1,2,3,4,5"

# Custom CSS
def get_theme_css(theme):
    if theme == "Dark":
        bg_color = "#0e1117"
        card_bg = "#1e1e1e"
        text_color = "#fafafa"
        heading_color = "#ffffff"
        border_color = "#333333"
        formula_bg = "#1e3a5f"
        formula_text = "#a8d5ff"
    else:
        bg_color = "#f5f7fa"
        card_bg = "#ffffff"
        text_color = "#2c3e50"
        heading_color = "#1a202c"
        border_color = "#e2e8f0"
        formula_bg = "#ebf8ff"
        formula_text = "#2c5282"
    
    return f"""
    <style>
        .stApp {{
            background-color: {bg_color} !important;
        }}
        .card {{
            background-color: {card_bg};
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border: 1px solid {border_color};
            margin-bottom: 20px;
        }}
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 16px;
            padding: 24px;
            text-align: center;
            color: white;
            box-shadow: 0 8px 16px rgba(102,126,234,0.4);
        }}
        .stat-card h3 {{
            color: white !important;
            font-size: 16px;
            font-weight: 600;
            margin: 0 0 8px 0;
        }}
        .stat-card .value {{
            color: white !important;
            font-size: 36px;
            font-weight: 700;
            margin: 0;
        }}
        .cache-cell {{
            background-color: {card_bg};
            border: 3px solid {border_color};
            border-radius: 12px;
            padding: 16px 12px;
            text-align: center;
            margin: 6px;
            min-height: 90px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            transition: all 0.3s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .cache-cell:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }}
        .hit {{
            background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%) !important;
            border: 3px solid #28a745 !important;
            color: #155724 !important;
            animation: pulse 0.5s ease;
        }}
        .miss {{
            background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%) !important;
            border: 3px solid #dc3545 !important;
            color: #721c24 !important;
            animation: shake 0.5s ease;
        }}
        .empty {{
            background-color: {card_bg} !important;
            border: 2px dashed {border_color} !important;
            color: #6c757d !important;
        }}
        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.05); }}
        }}
        @keyframes shake {{
            0%, 100% {{ transform: translateX(0); }}
            25% {{ transform: translateX(-5px); }}
            75% {{ transform: translateX(5px); }}
        }}
        .sequence-block {{
            display: inline-block;
            background-color: {card_bg};
            border: 2px solid {border_color};
            border-radius: 8px;
            padding: 12px 16px;
            margin: 4px;
            font-weight: 600;
            font-size: 18px;
            color: {text_color};
            transition: all 0.3s ease;
        }}
        .sequence-block.active {{
            background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
            border: 3px solid #f39c12;
            color: #000;
            transform: scale(1.15);
            box-shadow: 0 4px 12px rgba(243,156,18,0.5);
        }}
        .sequence-block.processed {{
            opacity: 0.5;
        }}
        .explanation-box {{
            background-color: {formula_bg};
            border-left: 5px solid #3498db;
            border-radius: 12px;
            padding: 20px;
            margin: 20px 0;
            font-size: 16px;
            line-height: 1.8;
            color: {formula_text};
            font-weight: 500;
            box-shadow: 0 2px 8px rgba(52,152,219,0.2);
        }}
        .block-label {{
            font-size: 13px;
            font-weight: 600;
            color: inherit;
            margin-bottom: 6px;
            opacity: 0.8;
        }}
        .block-content {{
            font-size: 22px;
            font-weight: 700;
            color: inherit;
        }}
        h1, h2, h3 {{
            color: {heading_color} !important;
        }}
        .stButton>button {{
            border-radius: 8px;
            font-weight: 600;
            padding: 8px 24px;
            transition: all 0.3s ease;
        }}
        .stButton>button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        .set-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white !important;
            padding: 12px 20px;
            border-radius: 10px;
            font-weight: 700;
            font-size: 16px;
            margin: 16px 0 12px 0;
            text-align: center;
        }}
    </style>
    """

st.markdown(get_theme_css(st.session_state.theme), unsafe_allow_html=True)

# Cache Classes
class CacheSimulator:
    def __init__(self, cache_size: int, replacement_policy: str):
        self.cache_size = cache_size
        self.replacement_policy = replacement_policy
        self.cache = {}
        self.hits = 0
        self.misses = 0
        self.access_history = []

class DirectMappedCache(CacheSimulator):
    def access(self, block: int) -> Tuple[bool, int, str]:
        index = block % self.cache_size
        is_hit = index in self.cache and self.cache[index] == block
        
        explanation = f"Block {block} → Index = {block} % {self.cache_size} = {index}"
        
        if is_hit:
            self.hits += 1
            explanation += f"<br>✓ <b>HIT</b>: Cache[{index}] contains Block {block}"
        else:
            self.misses += 1
            old_block = self.cache.get(index, None)
            self.cache[index] = block
            if old_block is not None:
                explanation += f"<br>✗ <b>MISS</b>: Cache[{index}] had Block {old_block}, replaced with Block {block}"
            else:
                explanation += f"<br>✗ <b>MISS</b>: Cache[{index}] was empty, loaded Block {block}"
        
        self.access_history.append((block, is_hit, index))
        return is_hit, index, explanation

class FullyAssociativeCache(CacheSimulator):
    def __init__(self, cache_size: int, replacement_policy: str):
        super().__init__(cache_size, replacement_policy)
        self.queue = []
        self.lru_counter = {}
        self.access_count = 0
        
    def access(self, block: int) -> Tuple[bool, int, str]:
        is_hit = block in self.cache.values()
        explanation = f"Block {block} → Search all cache lines"
        
        if is_hit:
            self.hits += 1
            index = [k for k, v in self.cache.items() if v == block][0]
            explanation += f"<br>✓ <b>HIT</b>: Found at Cache[{index}]"
            
            if self.replacement_policy == "LRU":
                self.lru_counter[index] = self.access_count
                self.access_count += 1
        else:
            self.misses += 1
            
            if len(self.cache) < self.cache_size:
                index = len(self.cache)
                self.cache[index] = block
                explanation += f"<br>✗ <b>MISS</b>: Loaded into Cache[{index}]"
            else:
                if self.replacement_policy == "FIFO":
                    index = self.queue.pop(0)
                    old_block = self.cache[index]
                    self.cache[index] = block
                    explanation += f"<br>✗ <b>MISS</b>: FIFO replaced Block {old_block} at Cache[{index}]"
                else:
                    index = min(self.lru_counter, key=self.lru_counter.get)
                    old_block = self.cache[index]
                    self.cache[index] = block
                    explanation += f"<br>✗ <b>MISS</b>: LRU replaced Block {old_block} at Cache[{index}]"
            
            if self.replacement_policy == "FIFO":
                self.queue.append(index)
            else:
                self.lru_counter[index] = self.access_count
                self.access_count += 1
        
        self.access_history.append((block, is_hit, index))
        return is_hit, index, explanation

class SetAssociativeCache(CacheSimulator):
    def __init__(self, cache_size: int, num_sets: int, replacement_policy: str):
        super().__init__(cache_size, replacement_policy)
        self.num_sets = num_sets
        self.lines_per_set = cache_size // num_sets
        self.sets = {i: {} for i in range(num_sets)}
        self.queue = {i: [] for i in range(num_sets)}
        self.lru_counter = {i: {} for i in range(num_sets)}
        self.access_count = 0
        
    def access(self, block: int) -> Tuple[bool, int, str]:
        set_index = block % self.num_sets
        explanation = f"Block {block} → Set = {block} % {self.num_sets} = {set_index}"
        
        is_hit = block in self.sets[set_index].values()
        
        if is_hit:
            self.hits += 1
            line = [k for k, v in self.sets[set_index].items() if v == block][0]
            cache_index = set_index * self.lines_per_set + line
            explanation += f"<br>✓ <b>HIT</b>: Found in Set {set_index}, Line {line}"
            
            if self.replacement_policy == "LRU":
                self.lru_counter[set_index][line] = self.access_count
                self.access_count += 1
        else:
            self.misses += 1
            
            if len(self.sets[set_index]) < self.lines_per_set:
                line = len(self.sets[set_index])
                self.sets[set_index][line] = block
                cache_index = set_index * self.lines_per_set + line
                explanation += f"<br>✗ <b>MISS</b>: Loaded into Set {set_index}, Line {line}"
            else:
                if self.replacement_policy == "FIFO":
                    line = self.queue[set_index].pop(0)
                    old_block = self.sets[set_index][line]
                    self.sets[set_index][line] = block
                    cache_index = set_index * self.lines_per_set + line
                    explanation += f"<br>✗ <b>MISS</b>: FIFO replaced Block {old_block} in Set {set_index}, Line {line}"
                else:
                    line = min(self.lru_counter[set_index], key=self.lru_counter[set_index].get)
                    old_block = self.sets[set_index][line]
                    self.sets[set_index][line] = block
                    cache_index = set_index * self.lines_per_set + line
                    explanation += f"<br>✗ <b>MISS</b>: LRU replaced Block {old_block} in Set {set_index}, Line {line}"
            
            if self.replacement_policy == "FIFO":
                self.queue[set_index].append(line)
            else:
                self.lru_counter[set_index][line] = self.access_count
                self.access_count += 1
        
        cache_index = set_index * self.lines_per_set + list(self.sets[set_index].keys())[list(self.sets[set_index].values()).index(block)]
        self.access_history.append((block, is_hit, cache_index))
        return is_hit, cache_index, explanation

# Title
st.markdown(f"<h1 style='text-align: center; margin-bottom: 10px;'>Cache Memory Visualizer</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #7f8c8d; margin-bottom: 30px;'>Interactive Learning Tool for Computer Organization & Architecture</p>", unsafe_allow_html=True)

# Controls Card
st.markdown('<div class="card">', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns([1.5, 1, 1.2, 1, 1])

with col1:
    mapping_type = st.selectbox("Mapping Type", ["Direct Mapping", "Fully Associative", "Set Associative"])

with col2:
    cache_size = st.number_input("Cache Size", min_value=2, max_value=32, value=8, step=1)

with col3:
    if mapping_type == "Set Associative":
        num_sets = st.number_input("Number of Sets", min_value=2, max_value=cache_size//2, value=4, step=1)
    else:
        num_sets = None
        st.markdown("<div style='height: 58px;'></div>", unsafe_allow_html=True)

with col4:
    replacement_policy = st.selectbox("Policy", ["FIFO", "LRU"]) if mapping_type != "Direct Mapping" else "N/A"
    if mapping_type == "Direct Mapping":
        st.markdown("<div style='height: 58px;'></div>", unsafe_allow_html=True)

with col5:
    theme = st.selectbox("Theme", ["Light", "Dark"], index=0 if st.session_state.theme == "Light" else 1)
    if theme != st.session_state.theme:
        st.session_state.theme = theme
        st.rerun()

st.markdown("---")

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    sequence_input = st.text_input("Memory Access Sequence (comma-separated)", value=st.session_state.sequence_input, key='seq_input')
    st.session_state.sequence_input = sequence_input

with col2:
    animation_mode = st.selectbox("Mode", ["Auto-Run", "Step-by-Step"])

with col3:
    if animation_mode == "Auto-Run":
        speed = st.slider("Speed (s)", 0.1, 2.0, 0.5, 0.1)
    else:
        speed = 0
        st.markdown("<div style='height: 58px;'></div>", unsafe_allow_html=True)

st.markdown("---")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("▶ Start", use_container_width=True, type="primary"):
        try:
            st.session_state.sequence = [int(x.strip()) for x in sequence_input.split(",") if x.strip()]
            
            if mapping_type == "Direct Mapping":
                st.session_state.simulator = DirectMappedCache(cache_size, "N/A")
            elif mapping_type == "Fully Associative":
                st.session_state.simulator = FullyAssociativeCache(cache_size, replacement_policy)
            else:
                st.session_state.simulator = SetAssociativeCache(cache_size, num_sets, replacement_policy)
            
            st.session_state.current_step = 0
            st.session_state.running = animation_mode == "Auto-Run"
            st.session_state.animation_mode = animation_mode
            st.session_state.step_processed = False
            st.rerun()
        except:
            st.error("Invalid sequence format")

with col2:
    if st.session_state.simulator and st.session_state.animation_mode == "Step-by-Step" and st.session_state.current_step < len(st.session_state.sequence):
        if st.button("⏭ Next Step", use_container_width=True):
            st.session_state.step_processed = False
            st.rerun()

with col3:
    if st.button("🔄 Reset", use_container_width=True):
        st.session_state.simulator = None
        st.session_state.current_step = 0
        st.session_state.running = False
        st.session_state.step_processed = False
        st.rerun()

with col4:
    if st.button("📋 Example", use_container_width=True):
        st.session_state.sequence_input = "1,2,3,4,1,2,5,1,2,3,4,5"
        st.rerun()

with col5:
    if st.button("🎲 Random", use_container_width=True):
        st.session_state.sequence_input = ",".join([str(random.randint(0, 15)) for _ in range(12)])
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Main Content
if st.session_state.simulator is None:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.info("Configure settings above and click Start to begin simulation")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("#### Direct Mapping")
        st.markdown("• Each block maps to one cache line<br>• Formula: `index = block % cache_size`<br>• Simple but prone to conflicts", unsafe_allow_html=True)
    with col2:
        st.markdown("#### Fully Associative")
        st.markdown("• Block can go in any cache line<br>• Most flexible<br>• Requires replacement policy", unsafe_allow_html=True)
    with col3:
        st.markdown("#### Set Associative")
        st.markdown("• Compromise between both<br>• Block maps to a set<br>• Formula: `set = block % num_sets`", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # Stats Cards
    total_accesses = st.session_state.current_step
    hit_ratio = (st.session_state.simulator.hits / total_accesses * 100) if total_accesses > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f'''<div class="stat-card">
            <h3>Total Accesses</h3>
            <div class="value">{total_accesses}</div>
        </div>''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''<div class="stat-card" style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);">
            <h3>Hits</h3>
            <div class="value">{st.session_state.simulator.hits}</div>
        </div>''', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''<div class="stat-card" style="background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);">
            <h3>Misses</h3>
            <div class="value">{st.session_state.simulator.misses}</div>
        </div>''', unsafe_allow_html=True)
    
    with col4:
        st.markdown(f'''<div class="stat-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <h3>Hit Ratio</h3>
            <div class="value">{hit_ratio:.1f}%</div>
        </div>''', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Sequence Visualization
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Memory Access Sequence")
    
    sequence_html = ""
    for i, block in enumerate(st.session_state.sequence):
        if i < st.session_state.current_step:
            css_class = "sequence-block processed"
        elif i == st.session_state.current_step:
            css_class = "sequence-block active"
        else:
            css_class = "sequence-block"
        sequence_html += f'<span class="{css_class}">{block}</span>'
    
    st.markdown(f'<div style="text-align: center; margin: 20px 0;">{sequence_html}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Process current step
    if st.session_state.current_step < len(st.session_state.sequence) and not st.session_state.step_processed:
        block = st.session_state.sequence[st.session_state.current_step]
        is_hit, cache_index, explanation = st.session_state.simulator.access(block)
        st.session_state.step_processed = True
        
        # Explanation
        st.markdown(f'<div class="explanation-box">{explanation}</div>', unsafe_allow_html=True)
        
        # Cache Visualization
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Cache State")
        
        if mapping_type == "Direct Mapping":
            num_cols = min(cache_size, 4)
            cols = st.columns(num_cols)
            for i in range(cache_size):
                with cols[i % num_cols]:
                    if i in st.session_state.simulator.cache:
                        block_val = st.session_state.simulator.cache[i]
                        css_class = "hit" if i == cache_index and is_hit else "miss" if i == cache_index else "empty"
                        st.markdown(f'''<div class="cache-cell {css_class}">
                            <div class="block-label">Index {i}</div>
                            <div class="block-content">Block {block_val}</div>
                        </div>''', unsafe_allow_html=True)
                    else:
                        st.markdown(f'''<div class="cache-cell empty">
                            <div class="block-label">Index {i}</div>
                            <div class="block-content">Empty</div>
                        </div>''', unsafe_allow_html=True)
        
        elif mapping_type == "Fully Associative":
            num_cols = min(cache_size, 4)
            cols = st.columns(num_cols)
            for i in range(cache_size):
                with cols[i % num_cols]:
                    if i in st.session_state.simulator.cache:
                        block_val = st.session_state.simulator.cache[i]
                        css_class = "hit" if i == cache_index and is_hit else "miss" if i == cache_index else "empty"
                        st.markdown(f'''<div class="cache-cell {css_class}">
                            <div class="block-label">Line {i}</div>
                            <div class="block-content">Block {block_val}</div>
                        </div>''', unsafe_allow_html=True)
                    else:
                        st.markdown(f'''<div class="cache-cell empty">
                            <div class="block-label">Line {i}</div>
                            <div class="block-content">Empty</div>
                        </div>''', unsafe_allow_html=True)
        
        else:  # Set Associative
            for set_idx in range(num_sets):
                st.markdown(f'<div class="set-header">Set {set_idx}</div>', unsafe_allow_html=True)
                cols = st.columns(cache_size // num_sets)
                for line in range(cache_size // num_sets):
                    with cols[line]:
                        if line in st.session_state.simulator.sets[set_idx]:
                            block_val = st.session_state.simulator.sets[set_idx][line]
                            global_idx = set_idx * (cache_size // num_sets) + line
                            css_class = "hit" if global_idx == cache_index and is_hit else "miss" if global_idx == cache_index else "empty"
                            st.markdown(f'''<div class="cache-cell {css_class}">
                                <div class="block-label">Line {line}</div>
                                <div class="block-content">Block {block_val}</div>
                            </div>''', unsafe_allow_html=True)
                        else:
                            st.markdown(f'''<div class="cache-cell empty">
                                <div class="block-label">Line {line}</div>
                                <div class="block-content">Empty</div>
                            </div>''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Auto-advance
        if st.session_state.animation_mode == "Auto-Run":
            time.sleep(speed)
            st.session_state.current_step += 1
            st.session_state.step_processed = False
            
            if st.session_state.current_step < len(st.session_state.sequence):
                st.rerun()
            else:
                st.session_state.running = False
                st.success("✅ Simulation Complete!")
                st.balloons()
        else:
            st.session_state.current_step += 1
    
    elif st.session_state.current_step >= len(st.session_state.sequence):
        st.success("✅ Simulation Complete!")
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Final Statistics")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Hits", st.session_state.simulator.hits)
            st.metric("Hit Ratio", f"{hit_ratio:.2f}%")
        with col2:
            st.metric("Total Misses", st.session_state.simulator.misses)
            st.metric("Miss Ratio", f"{100-hit_ratio:.2f}%")
        st.markdown('</div>', unsafe_allow_html=True)
