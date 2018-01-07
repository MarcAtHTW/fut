Create View view_fut_watchlist as
Select w2.*
	From (
		Select w.resourceId, count(*) as anzahl
		From fut_watchlist w
		-- where resourceId in ('9014', '41236', '238431')
		group by resourceId
	) as a, fut_watchlist w2
Where a.anzahl>999
and a.resourceId=w2.resourceId