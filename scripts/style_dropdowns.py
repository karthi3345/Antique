import re

with open('static/css/volgo.css', encoding='utf-8') as f:
    css = f.read()

# Enhance select dropdown styling
select_enhancements = """
/* Premium Royal Dropdowns */
.field select {
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23C3A24B' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right center;
  background-size: 16px;
  padding-right: 32px;
  cursor: pointer;
  border-bottom: 1px solid var(--gold);
}

.field select:hover {
  border-bottom-color: var(--gold-pale);
}

.field select option {
  background-color: var(--cream);
  color: var(--ivory);
  padding: 12px;
  font-family: var(--font-body);
  font-size: 16px;
}
"""

css += select_enhancements

with open('static/css/volgo.css', 'w', encoding='utf-8') as f:
    f.write(css)
