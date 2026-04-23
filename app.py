import streamlit as st
import time
import random
from typing import List, Tuple, Dict

# Page config
st.set_page_config(page_title="Cache Memory Visualizer", layout="wide", initial_sidebar_state="expanded")

# Initialize session state first
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

# Custom CSS
def get_theme_css(theme):
    if theme == "Dark":
        bg_color = "#0e1117"
        text_color = "#fafafa"
        heading_color = "#ffffff"
        metric_bg = "#262730"
        metric_border = "#4a4a4a"
        formula_bg = "#1e3a5f"
        formula_text = "#a8d5ff"
        set_label_bg = "#262730"
        set_label_border = "#4a4a4a"
        sidebar_bg = "#262730"
        sidebar_text = "#fafafa"
    else:  # Light
        bg_color = "#ffffff"
        text_color = "#262730"
        heading_color = "#262730"
        metric_bg = "#ffffff"
        metric_border = "#dee2e6"
        formula_bg = "#e7f3ff"
        formula_text = "#0d47a1"
        set_label_bg = "#e9ecef"
        set_label_border = "#adb5bd"
        sidebar_bg = "#f8f9fa"
        sidebar_text = "#262730"
    
    return f"""
    <style>
        .stApp {{
            background-color: {bg_color} !important;
        }}
        section[data-testid="stSidebar"] {{
            background-color: {sidebar_bg} !important;
        }}
        section[data-testid="stSidebar"] label {{
            color: {sidebar_text} !important;
        }}
        section[data-testid="stSidebar"] .stMarkdown {{
            color: {sidebar_text} !important;
        }}
        section[data-testid="stSidebar"] h1, 
        section[data-testid="stSidebar"] h2, 
        section[data-testid="stSidebar"] h3 {{
            color: {heading_color} !important;
        }}
        section[data-testid="stSidebar"] input {{
            background-color: {metric_bg} !important;
            color: {text_color} !important;
            border-color: {metric_border} !important;
        }}
        section[data-testid="stSidebar"] textarea {{
            background-color: {metric_bg} !important;
            color: {text_color} !important;
            border-color: {metric_border} !important;
        }}
        section[data-testid="stSidebar"] select {{
            background-color: {metric_bg} !important;
            color: {text_color} !important;
        }}
        section[data-testid="stSidebar"] .stSelectbox label {{
            color: {sidebar_text} !important;
        }}
        section[data-testid="stSidebar"] .stNumberInput label {{
            color: {sidebar_text} !important;
        }}
        section[data-testid="stSidebar"] .stTextArea label {{
            color: {sidebar_text} !important;
        }}
        .cache-cell {{
            padding: 20px 10px;
            border-radius: 8px;
            text-align: center;
            margin: 8px 2px;
            font-weight: 600;
            font-size: 16px;
            min-height: 80px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }}
        .hit {{ 
            background-color: #d4edda !important; 
            border: 3px solid #28a745 !important;
            color: #155724 !important;
        }}
        .miss {{ 
            background-color: #f8d7da !important; 
            border: 3px solid #dc3545 !important;
            color: #721c24 !important;
        }}
        .empty {{ 
            background-color: #f8f9fa !important; 
            border: 2px dashed #dee2e6 !important;
            color: #6c757d !important;
        }}
        .formula-box {{
            padding: 20px;
            background-color: {formula_bg};
            border-left: 5px solid #2196F3;
            border-radius: 8px;
            margin: 15px 0;
            font-size: 16px;
            line-height: 1.8;
            color: {formula_text};
            font-weight: 500;
        }}
        .stMetric {{
            background-color: {metric_bg} !important;
            padding: 20px !important;
            border-radius: 10px !important;
            border: 2px solid {metric_border} !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
        }}
        .stMetric label {{
            font-size: 18px !important;
            font-weight: 600 !important;
            color: {text_color} !important;
        }}
        .stMetric [data-testid="stMetricValue"] {{
            font-size: 36px !important;
            font-weight: 700 !important;
            color: {heading_color} !important;
        }}
        .stMetric [data-testid="stMetricDelta"] {{
            font-size: 16px !important;
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: {heading_color} !important;
            font-weight: 700 !important;
        }}
        p, span, div {{
            color: {text_color} !important;
        }}
        .set-label {{
            font-size: 18px;
            font-weight: 700;
            color: {heading_color} !important;
            margin: 20px 0 10px 0;
            padding: 12px;
            background-color: {set_label_bg};
            border-radius: 5px;
            border: 2px solid {set_label_border};
        }}
        .block-content {{
            font-size: 20px !important;
            font-weight: 700 !important;
            color: inherit !important;
            margin-top: 5px !important;
        }}
        .block-label {{
            font-size: 14px !important;
            font-weight: 600 !important;
            color: inherit !important;
            margin-bottom: 5px !important;
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
        
    def reset(self):
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
            explanation += f"\n✓ HIT: Cache[{index}] contains Block {block}"
        else:
            self.misses += 1
            old_block = self.cache.get(index, None)
            self.cache[index] = block
            if old_block is not None:
                explanation += f"\n✗ MISS: Cache[{index}] had Block {old_block}, replaced with Block {block}"
            else:
                explanation += f"\n✗ MISS: Cache[{index}] was empty, loaded Block {block}"
        
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
            explanation += f"\n✓ HIT: Found at Cache[{index}]"
            
            if self.replacement_policy == "LRU":
                self.lru_counter[index] = self.access_count
                self.access_count += 1
        else:
            self.misses += 1
            
            if len(self.cache) < self.cache_size:
                index = len(self.cache)
                self.cache[index] = block
                explanation += f"\n✗ MISS: Loaded into Cache[{index}]"
            else:
                if self.replacement_policy == "FIFO":
                    index = self.queue.pop(0)
                    old_block = self.cache[index]
                    self.cache[index] = block
                    explanation += f"\n✗ MISS: FIFO replaced Block {old_block} at Cache[{index}] with Block {block}"
                else:  # LRU
                    index = min(self.lru_counter, key=self.lru_counter.get)
                    old_block = self.cache[index]
                    self.cache[index] = block
                    explanation += f"\n✗ MISS: LRU replaced Block {old_block} at Cache[{index}] with Block {block}"
            
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
            explanation += f"\n✓ HIT: Found in Set {set_index}, Line {line}"
            
            if self.replacement_policy == "LRU":
                self.lru_counter[set_index][line] = self.access_count
                self.access_count += 1
        else:
            self.misses += 1
            
            if len(self.sets[set_index]) < self.lines_per_set:
                line = len(self.sets[set_index])
                self.sets[set_index][line] = block
                cache_index = set_index * self.lines_per_set + line
                explanation += f"\n✗ MISS: Loaded into Set {set_index}, Line {line}"
            else:
                if self.replacement_policy == "FIFO":
                    line = self.queue[set_index].pop(0)
                    old_block = self.sets[set_index][line]
                    self.sets[set_index][line] = block
                    cache_index = set_index * self.lines_per_set + line
                    explanation += f"\n✗ MISS: FIFO replaced Block {old_block} in Set {set_index}, Line {line}"
                else:  # LRU
                    line = min(self.lru_counter[set_index], key=self.lru_counter[set_index].get)
                    old_block = self.sets[set_index][line]
                    self.sets[set_index][line] = block
                    cache_index = set_index * self.lines_per_set + line
                    explanation += f"\n✗ MISS: LRU replaced Block {old_block} in Set {set_index}, Line {line}"
            
            if self.replacement_policy == "FIFO":
                self.queue[set_index].append(line)
            else:
                self.lru_counter[set_index][line] = self.access_count
                self.access_count += 1
        
        cache_index = set_index * self.lines_per_set + list(self.sets[set_index].keys())[list(self.sets[set_index].values()).index(block)]
        self.access_history.append((block, is_hit, cache_index))
        return is_hit, cache_index, explanation

# Title
st.title("Cache Memory Visualizer")
st.markdown("*Interactive Learning Tool for Computer Organization & Architecture*")

# Sidebar
with st.sidebar:
    st.header("Configuration")
    
    # Theme toggle
    theme_col1, theme_col2 = st.columns([3, 1])
    with theme_col1:
        theme = st.selectbox("Theme", ["Light", "Dark"], index=0 if st.session_state.theme == "Light" else 1, label_visibility="collapsed")
    with theme_col2:
        if st.button("🌓"):
            st.session_state.theme = "Dark" if st.session_state.theme == "Light" else "Light"
            st.rerun()
    
    if theme != st.session_state.theme:
        st.session_state.theme = theme
        st.rerun()
    
    st.markdown("---")
    
    mapping_type = st.selectbox(
        "Mapping Type",
        ["Direct Mapping", "Fully Associative", "Set Associative"]
    )
    
    cache_size = st.number_input("Cache Size (lines)", min_value=2, max_value=32, value=8, step=1)
    
    num_sets = None
    if mapping_type == "Set Associative":
        num_sets = st.number_input("Number of Sets", min_value=2, max_value=cache_size//2, value=4, step=1)
        st.info(f"Lines per set: {cache_size // num_sets}")
    
    replacement_policy = st.selectbox(
        "Replacement Policy",
        ["FIFO", "LRU"]
    ) if mapping_type != "Direct Mapping" else "N/A"
    
    st.markdown("---")
    st.subheader("Memory Access Sequence")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Example 1"):
            st.session_state.sequence_input = "1,2,3,4,1,2,5,1,2,3,4,5"
    with col2:
        if st.button("Random"):
            st.session_state.sequence_input = ",".join([str(random.randint(0, 15)) for _ in range(12)])
    
    sequence_input = st.text_area(
        "Enter sequence (comma-separated)",
        value=st.session_state.get('sequence_input', "1,2,3,4,1,2,5,1,2,3,4,5"),
        height=100,
        key='sequence_input'
    )
    
    st.markdown("---")
    st.subheader("Controls")
    
    animation_mode = st.radio(
        "Animation Mode",
        ["Auto-Run", "Step-by-Step"],
        horizontal=True
    )
    
    if animation_mode == "Auto-Run":
        speed = st.slider("Animation Speed (seconds)", 0.1, 2.0, 0.5, 0.1)
    else:
        speed = 0
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Start", use_container_width=True):
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
        if st.button("Reset", use_container_width=True):
            st.session_state.simulator = None
            st.session_state.current_step = 0
            st.session_state.running = False
            st.session_state.step_processed = False
            st.rerun()
    
    if st.session_state.simulator and st.session_state.current_step < len(st.session_state.sequence):
        if st.session_state.animation_mode == "Step-by-Step":
            if st.button("Next Step", use_container_width=True, type="primary"):
                st.session_state.step_processed = False
                st.rerun()

# Main area
if st.session_state.simulator is None:
    st.info("Configure settings in the sidebar and click Start to begin simulation")
    
    # Educational content
    st.markdown("### Cache Mapping Techniques")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### Direct Mapping")
        st.markdown("""
        - Each block maps to exactly one cache line
        - Formula: `index = block % cache_size`
        - Simple but prone to conflicts
        """)
    
    with col2:
        st.markdown("#### Fully Associative")
        st.markdown("""
        - Block can go in any cache line
        - Most flexible
        - Requires replacement policy
        """)
    
    with col3:
        st.markdown("#### Set Associative")
        st.markdown("""
        - Compromise between both
        - Block maps to a set, any line in set
        - Formula: `set = block % num_sets`
        """)

else:
    # Stats
    total_accesses = st.session_state.current_step
    hit_ratio = (st.session_state.simulator.hits / total_accesses * 100) if total_accesses > 0 else 0
    miss_ratio = 100 - hit_ratio
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Accesses", total_accesses)
    with col2:
        st.metric("Hits", st.session_state.simulator.hits, delta=None, delta_color="normal")
    with col3:
        st.metric("Misses", st.session_state.simulator.misses, delta=None, delta_color="inverse")
    with col4:
        st.metric("Hit Ratio", f"{hit_ratio:.1f}%")
    
    st.markdown("---")
    
    # Process current step
    if st.session_state.current_step < len(st.session_state.sequence) and not st.session_state.step_processed:
        block = st.session_state.sequence[st.session_state.current_step]
        is_hit, cache_index, explanation = st.session_state.simulator.access(block)
        st.session_state.step_processed = True
        
        # Show current access
        st.markdown(f"### Step {st.session_state.current_step + 1}: Accessing Block **{block}**")
        
        # Explanation
        st.markdown(f'<div class="formula-box">{explanation.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
        
        # Visualize cache
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
                st.markdown(f'<div class="set-label">Set {set_idx}</div>', unsafe_allow_html=True)
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
        
        # Auto-advance for Auto-Run mode
        if st.session_state.animation_mode == "Auto-Run":
            time.sleep(speed)
            st.session_state.current_step += 1
            st.session_state.step_processed = False
            
            if st.session_state.current_step < len(st.session_state.sequence):
                st.rerun()
            else:
                st.session_state.running = False
                st.success("Simulation Complete!")
                st.balloons()
        else:
            # Step-by-step mode - increment after display
            st.session_state.current_step += 1
    
    elif st.session_state.current_step >= len(st.session_state.sequence):
        st.success("Simulation Complete!")
        
        # Final stats
        st.markdown("### Final Statistics")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Hits", st.session_state.simulator.hits)
            st.metric("Hit Ratio", f"{hit_ratio:.2f}%")
        with col2:
            st.metric("Total Misses", st.session_state.simulator.misses)
            st.metric("Miss Ratio", f"{miss_ratio:.2f}%")
