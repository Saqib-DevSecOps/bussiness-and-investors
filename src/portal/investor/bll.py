from decimal import Decimal

from src.portal.business.models import MoneyFlow, Investor,Project_Investor


def money_flow(self, request):
    user = request.user
    b_profit = 0
    b_loss = 0
    i_profit = 0
    i_loss = 0
    if Project_Investor.objects.filter(investor__user = user):
        value = MoneyFlow.objects.filter(project_investor__investor__user=request.user)
  
        if value:
            for value in value:
                b_profit = Decimal(value.business_profit_project) + Decimal(b_profit)
                b_loss = Decimal(value.business_loss_project) + Decimal(b_loss)
                i_profit = Decimal(value.investor_profit) + Decimal(i_profit)
                i_loss = Decimal(value.investor_loss) + Decimal(i_loss)
                return b_profit, b_loss, i_profit, i_loss
        else:
            return b_profit, b_loss, i_profit, i_loss  
    else:
        return b_profit, b_loss, i_profit, i_loss
