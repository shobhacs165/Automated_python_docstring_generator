# app.py - COMPLETE + Source + Generated Docstrings TOGETHER
import tempfile
from pathlib import Path
import streamlit as st
import matplotlib.pyplot as plt

from automated_docstrings.parser import parse_module
from automated_docstrings.synthesizer import (
    synthesize_function_doc,
    synthesize_class_doc,
)
from automated_docstrings.reporting import analyze_file

STYLE_OPTIONS = ["Google", "NumPy", "reST"]

def create_validation_graphs(coverage, compliance, filename):
    """PPT-style compliance/coverage graphs"""
    total_symbols = coverage["total_symbols"]
    documented = coverage["documented_symbols"]
    undocumented = total_symbols - documented
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Coverage Pie Chart
    colors = ['#10B981', '#EF4444']
    ax1.pie([documented, undocumented], labels=['Documented', 'Undocumented'], 
            colors=colors, autopct='%1.1f%%', startangle=90)
    ax1.set_title(f'{filename}\nDocumentation Coverage')
    
    # Compliance Bar Chart
    total_issues = compliance["issue_count"]
    max_issues = total_symbols * 3
    compliance_pct = max(0, 100 * (1 - total_issues / max_issues))
    
    issues = ['Compliant %', 'Issues %']
    counts = [compliance_pct, 100 - compliance_pct]
    bars = ax2.bar(issues, counts, color=['#10B981', '#F59E0B'])
    ax2.set_ylabel('Percentage')
    ax2.set_title(f'{filename}\npydocstyle Compliance')
    ax2.set_ylim(0, 100)
    
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.1f}%', ha='center', va='bottom')
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

def main():
    st.title("🚀 Automated Docstring Synthesis & Validation (Milestone 2)")

    st.sidebar.header("⚙️ Configuration")
    style = st.sidebar.selectbox("Docstring Style", STYLE_OPTIONS, index=0)
    run_validation = st.sidebar.checkbox("Run pydocstyle validation", value=True)

    uploaded_files = st.file_uploader(
        "📁 Upload Python file(s)",
        type=["py"],
        accept_multiple_files=True,
    )

    if not uploaded_files:
        st.info("👆 Upload .py file to analyze.")
        return

    for uploaded in uploaded_files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp:
            tmp.write(uploaded.read())
            tmp_path = Path(tmp.name)

        module = parse_module(tmp_path)
        report = analyze_file(tmp_path)
        coverage = report["coverage"]
        compliance = report["compliance"]

        # 📊 Compliance & Coverage Report
        st.markdown(f"### 📊 **Compliance & Coverage - {uploaded.name}**")
        total_symbols = coverage["total_symbols"]
        documented = coverage["documented_symbols"]
        doc_pct = coverage["coverage_percent"]
        
        total_issues = compliance["issue_count"]
        max_issues = total_symbols * 3
        compliance_pct = max(0, round(100 * (1 - total_issues / max_issues), 1)) if total_symbols > 0 else 0
        
        st.markdown(f"""
        **Total Functions:** {coverage['total_functions']}  
        **Total Classes:** {coverage['total_classes']}  
        **Documented:** {documented} vs **Undocumented:** {total_symbols - documented}  
        **Documentation %:** {doc_pct}%  
        **pydocstyle Compliance %:** {compliance_pct}%  
        **Total Issues:** {total_issues}
        """)

        # 📈 Validation Graphs (PPT Style)
        st.markdown("### 📈 **Validation Results**")
        create_validation_graphs(coverage, compliance, uploaded.name)

        # 🔗 SOURCE + GENERATED DOCSTRINGS COMBINED
        st.markdown("### 🔗 **Complete Code with Generated Docstrings**")
        source_code = tmp_path.read_text(encoding='utf-8')
        
        # Create combined code (original + docstrings inserted)
        combined_lines = []
        lines = source_code.split('\n')
        func_map = {f.lineno: f for f in module.functions}
        class_map = {c.lineno: c for c in module.classes}
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Check if function/class definition
            if line.lstrip().startswith('def ') or line.lstrip().startswith('class '):
                lineno = i + 1  # 1-based line number
                
                # Insert generated docstring
                if lineno in func_map:
                    func = func_map[lineno]
                    doc = synthesize_function_doc(func, style=style)
                    combined_lines.append(line)
                    combined_lines.append('    """')
                    for doc_line in doc.split('\n'):
                        combined_lines.append(f"    {doc_line}")
                    combined_lines.append('    """')
                elif lineno in class_map:
                    cls = class_map[lineno]
                    doc = synthesize_class_doc(cls, style=style)
                    combined_lines.append(line)
                    combined_lines.append('    """')
                    for doc_line in doc.split('\n'):
                        combined_lines.append(f"    {doc_line}")
                    combined_lines.append('    """')
                else:
                    combined_lines.append(line)
            else:
                combined_lines.append(line)
            
            i += 1
        
        combined_code = '\n'.join(combined_lines)
        st.code(combined_code, language="python")

        # 🔍 pydocstyle Issues
        if run_validation:
            st.markdown("### 🔍 **pydocstyle Issues (PEP 257)**")
            if compliance["issue_count"] == 0:
                st.success("✅ **100% PEP 257 Compliant**")
            else:
                st.error(f"🚨 **{compliance['issue_count']} violations** ({compliance_pct}% compliance)")
                for issue in compliance["issues"][:5]:
                    st.error(f"[{issue['code']}] L{issue['line']}: {issue['message']}")

        st.markdown("---")

if __name__ == "__main__":
    main()
