
SOURCE_DIR = ../2022

REVENUE_FILE = 01_revenue.toml
EXPENSE_FILE = 02_expenses.toml

REVENUE_PATH = $(SOURCE_DIR)/$(REVENUE_FILE)
EXPENSE_PATH = $(SOURCE_DIR)/$(EXPENSE_FILE)

all: csv revenue_monthly expenses_monthly expenses_category expenses_tags profit_monthly

csv:
	@echo "Generating CSV equivalent..."
	python3 scripts/export_toml_to_csv.py $(REVENUE_PATH) > /dev/null
	python3 scripts/export_toml_to_csv.py $(REVENUE_PATH) > $(REVENUE_FILE).csv
	python3 scripts/export_toml_to_csv.py $(EXPENSE_PATH) > /dev/null
	python3 scripts/export_toml_to_csv.py $(EXPENSE_PATH) > $(EXPENSE_FILE).csv
	@echo

revenue_monthly: $(REVENUE_PATH)
	@echo "Generating Revenue Graph..."
	python3 scripts/gen_monthly_revenue_graph.py $(REVENUE_PATH)
	@echo

expenses_monthly: $(EXPENSE_PATH)
	@echo "Generating Expense Graph..."
	python3 scripts/gen_monthly_expenses_graph.py $(EXPENSE_PATH)
	@echo

expenses_category: $(EXPENSE_PATH)
	@echo "Generating Expense Category Graph..."
	python3 scripts/gen_category_graph.py $(EXPENSE_PATH)
	@echo

expenses_tags: $(EXPENSE_PATH)
	@echo "Generating Expense Tag Graph..."
	python3 scripts/gen_tags_graph.py $(EXPENSE_PATH)
	@echo

profit_monthly:
	@echo "Generating Profit Graph..."
	python3 scripts/gen_monthly_profit_graph.py $(EXPENSE_PATH) $(REVENUE_PATH)
	@echo

clean:
	rm -f *.png *.csv
