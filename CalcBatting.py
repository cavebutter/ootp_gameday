CalcBatting = """CREATE TABLE IF NOT EXISTS CalcBatting (
    bat_id INT AUTO_INCREMENT PRIMARY KEY)
    SELECT b.year
    , b.level_id
    , b.league_id
    , b.player_id
    , b.stint
    , b.split_id
    , b.team_id
    , b.sub_league_id
    , b.g
    , b.ab
    , @PA := b.ab+b.bb+b.sh+b.sf+b.hp AS PA
    , b.r
    , b.h
    , b.d
    , b.t
    , b.hr
    , b.rbi
    , b.sb
    , b.cs
    , b.bb
    , b.k
    , b.ibb
    , b.hp
    , b.sh
    , b.sf
    , b.gdp
    , b.ci
    , b.war
    , @BA := round(b.h/b.ab,3) AS ba
    , IF(@PA=0,NULL,round(b.k/@PA,3)) as krate
    , IF(@PA=0,NULL,round((b.bb)/@PA,3)) as bbrate
    , @OBP := IF(@PA-b.sh-b.ci=0,NULL, round((b.h + b.bb + b.hp)/(@PA-b.sh-b.ci),3)) AS obp
    , IF(r.woba=0,NULL,round(100*(@OBP/r.woba),0)) as OBPplus
    , @SLG := round((b.h+b.d+2*b.t+3*b.hr)/b.ab,3) as slg
    , round(@OBP+@SLG,3) as ops
    , round(@SLG-@BA,3) as iso
    , IF(b.ab-b.k-b.hr+b.sf=0,0, round((b.h-b.hr)/(b.ab-b.k-b.hr+b.sf),3)) as babip
    , @woba := round((r.wobaBB*(b.bb-b.ibb) + r.wobaHB*b.hp + r.woba1B*(b.h-b.d-b.t-b.hr) + r.woba2B*b.d + r.woba3B*b.t + r.wobaHR*b.hr) / (b.ab+b.bb-b.ibb+b.sf+b.hp),3) as woba
    , @wRAA := round(((@woba-r.woba)/r.wOBAscale)*@PA,1) as wRAA
    , round((((@woba-r.woba)/r.wOBAscale)+(lro.totr/lro.totpa))*@PA,1) as wRC
    , ROUND((((@wRAA/@PA + lro.RperPA) + (lro.RperPA - p.avg*lro.RperPA))/(slg.slg_r/slg.slg_pa))*100,0) as 'wRC+'

    FROM
      players_career_batting_stats b
      INNER JOIN teams t ON b.team_id=t.team_id
      #INNER JOIN team_relations AS tr ON b.team_id=tr.team_id AND b.league_id=tr.league_id
      INNER JOIN tblRunValues2 r ON b.year=r.year AND b.league_id=r.league_id AND b.sub_league_id=r.sub_league_id
      INNER JOIN LeagueRunsPerOut lro ON b.year=lro.year AND b.league_id=lro.league_id AND b.sub_league_id=lro.sub_league_id
      INNER JOIN parks p ON t.park_id=p.park_id
      INNER JOIN sub_league_history_batting slg ON b.sub_league_id=slg.sub_league_id AND b.league_id=slg.league_id AND b.year=slg.year
    WHERE b.ab<>0 AND b.split_id=1 AND b.league_id<>0 AND b.team_id<>0
    ORDER BY b.player_id, b.year"""

CalcBatting_L = """CREATE TABLE IF NOT EXISTS CalcBatting_L (
    bat_id INT AUTO_INCREMENT PRIMARY KEY)
    SELECT b.year
    , b.level_id
    , b.league_id
    , b.player_id
    , b.stint
    , b.split_id
    , b.team_id
    , b.sub_league_id
    , b.g
    , b.ab
    , @PA := b.ab+b.bb+b.sh+b.sf+b.hp AS PA
    , b.r
    , b.h
    , b.d
    , b.t
    , b.hr
    , b.rbi
    , b.sb
    , b.cs
    , b.bb
    , b.k
    , b.ibb
    , b.hp
    , b.sh
    , b.sf
    , b.gdp
    , b.ci
    , b.war
    , @BA := round(b.h/b.ab,3) AS ba
    , IF(@PA=0,NULL,round(b.k/@PA,3)) as krate
    , IF(@PA=0,NULL,round((b.bb)/@PA,3)) as bbrate
    , @OBP := IF(@PA-b.sh-b.ci=0,NULL, round((b.h + b.bb + b.hp)/(@PA-b.sh-b.ci),3)) AS obp
    , IF(r.woba=0,NULL,round(100*(@OBP/r.woba),0)) as OBPplus
    , @SLG := round((b.h+b.d+2*b.t+3*b.hr)/b.ab,3) as slg
    , round(@OBP+@SLG,3) as ops
    , round(@SLG-@BA,3) as iso
    , IF(b.ab-b.k-b.hr+b.sf=0,0, round((b.h-b.hr)/(b.ab-b.k-b.hr+b.sf),3)) as babip
    , @woba := round((r.wobaBB*(b.bb-b.ibb) + r.wobaHB*b.hp + r.woba1B*(b.h-b.d-b.t-b.hr) + r.woba2B*b.d + r.woba3B*b.t + r.wobaHR*b.hr) / (b.ab+b.bb-b.ibb+b.sf+b.hp),3) as woba
    , @wRAA := round(((@woba-r.woba)/r.wOBAscale)*@PA,1) as wRAA
    , round((((@woba-r.woba)/r.wOBAscale)+(lro.totr/lro.totpa))*@PA,1) as wRC
    , ROUND((((@wRAA/@PA + lro.RperPA) + (lro.RperPA - p.avg*lro.RperPA))/(slg.slg_r/slg.slg_pa))*100,0) as 'wRC+'
    FROM
      players_career_batting_stats b
      INNER JOIN teams t ON b.team_id=t.team_id
      #INNER JOIN team_relations AS tr ON b.team_id=tr.team_id AND b.league_id=tr.league_id
      INNER JOIN tblRunValues2 r ON b.year=r.year AND b.league_id=r.league_id AND b.sub_league_id=r.sub_league_id
      INNER JOIN LeagueRunsPerOut lro ON b.year=lro.year AND b.league_id=lro.league_id AND b.sub_league_id=lro.sub_league_id
      INNER JOIN parks p ON t.park_id=p.park_id
      INNER JOIN sub_league_history_batting slg ON b.sub_league_id=slg.sub_league_id AND b.league_id=slg.league_id AND b.year=slg.year
    WHERE b.ab<>0 AND b.split_id=2 AND b.league_id<>0 AND b.team_id<>0
    ORDER BY b.player_id, b.year"""

CalcBatting_R = """CREATE TABLE IF NOT EXISTS CalcBatting_R (
    bat_id INT AUTO_INCREMENT PRIMARY KEY)
    SELECT b.year
    , b.level_id
    , b.league_id
    , b.player_id
    , b.stint
    , b.split_id
    , b.team_id
    , b.sub_league_id
    , b.g
    , b.ab
    , @PA := b.ab+b.bb+b.sh+b.sf+b.hp AS PA
    , b.r
    , b.h
    , b.d
    , b.t
    , b.hr
    , b.rbi
    , b.sb
    , b.cs
    , b.bb
    , b.k
    , b.ibb
    , b.hp
    , b.sh
    , b.sf
    , b.gdp
    , b.ci
    , b.war
    , @BA := round(b.h/b.ab,3) AS ba
    , IF(@PA=0,NULL,round(b.k/@PA,3)) as krate
    , IF(@PA=0,NULL,round((b.bb)/@PA,3)) as bbrate
    , @OBP := IF(@PA-b.sh-b.ci=0,NULL, round((b.h + b.bb + b.hp)/(@PA-b.sh-b.ci),3)) AS obp
    , IF(r.woba=0,NULL,round(100*(@OBP/r.woba),0)) as OBPplus
    , @SLG := round((b.h+b.d+2*b.t+3*b.hr)/b.ab,3) as slg
    , round(@OBP+@SLG,3) as ops
    , round(@SLG-@BA,3) as iso
    , IF(b.ab-b.k-b.hr+b.sf=0,0, round((b.h-b.hr)/(b.ab-b.k-b.hr+b.sf),3)) as babip
    , @woba := round((r.wobaBB*(b.bb-b.ibb) + r.wobaHB*b.hp + r.woba1B*(b.h-b.d-b.t-b.hr) + r.woba2B*b.d + r.woba3B*b.t + r.wobaHR*b.hr) / (b.ab+b.bb-b.ibb+b.sf+b.hp),3) as woba
    , @wRAA := round(((@woba-r.woba)/r.wOBAscale)*@PA,1) as wRAA
    , round((((@woba-r.woba)/r.wOBAscale)+(lro.totr/lro.totpa))*@PA,1) as wRC
    , ROUND((((@wRAA/@PA + lro.RperPA) + (lro.RperPA - p.avg*lro.RperPA))/(slg.slg_r/slg.slg_pa))*100,0) as 'wRC+'
    FROM
      players_career_batting_stats b
      INNER JOIN teams t ON b.team_id=t.team_id
      #INNER JOIN team_relations AS tr ON b.team_id=tr.team_id AND b.league_id=tr.league_id
      INNER JOIN tblRunValues2 r ON b.year=r.year AND b.league_id=r.league_id AND b.sub_league_id=r.sub_league_id
      INNER JOIN LeagueRunsPerOut lro ON b.year=lro.year AND b.league_id=lro.league_id AND b.sub_league_id=lro.sub_league_id
      INNER JOIN parks p ON t.park_id=p.park_id
      INNER JOIN sub_league_history_batting slg ON b.sub_league_id=slg.sub_league_id AND b.league_id=slg.league_id AND b.year=slg.year    WHERE b.ab<>0 AND b.split_id=3 AND b.league_id<>0 AND b.team_id<>0
    ORDER BY b.player_id, b.year"""

CalcPitching = """CREATE TABLE IF NOT EXISTS CalcPitching (pit_id INT AUTO_INCREMENT PRIMARY KEY)
SELECT
    i.player_id
    , i.year
    , i.stint
    , i.team_id
    , i.level_id
    , i.league_id
    , i.sub_league_id
    , i.split_id
    , i.ip
    , i.ab
    , i.tb
    , i.ha
    , i.k
    , i.bf
    , i.rs
    , i.bb
    , i.r
    , i.er
    , i.gb
    , i.fb
    , i.pi
    , i.ipf
    , i.g
    , i.gs
    , i.w
    , i.l
    , i.s
    , i.sa
    , i.da
    , i.sh
    , i.sf
    , i.ta
    , i.hra
    , i.bk
    , i.ci
    , i.iw
    , i.wp
    , i.hp
    , i.gf
    , i.dp
    , i.qs
    , i.svo
    , i.bs
    , i.ra
    , i.cg
    , i.sho
    , i.sb
    , i.cs
    , i.hld
    , i.ir
    , i.irs
    , i.wpa
    , i.li
    , i.outs
    , i.war
    , @InnPitch := ((3*ip)+ipf)/3 AS InnPitch
    , IF(@InnPitch=0,0,round((9*i.k)/@InnPitch,1)) AS 'k9'
    , IF(@InnPitch=0,0, round((9*i.bb)/@InnPitch,1)) AS 'bb9'
    , IF(@InnPitch=0,0,round((9*i.hra)/@InnPitch,1)) AS 'HR9'
    , IF(@InnPitch=0,0, round((i.bb+i.ha)/@InnPitch,2)) AS WHIP
    , IF(i.bb=0,0,round(i.k/i.bb,2)) AS 'K/BB'
    , IF(i.fb=0,0,i.gb/i.fb) AS 'gb/fb'
    , IF(i.ab-i.k-i.hra-i.sh+i.sf=0,0,round((i.ha-i.hra)/(i.ab-i.k-i.hra-i.sh+i.sf),3)) AS BABIP
    , IF(@InnPitch=0,0,@ERA := round((i.er/@InnPitch)*9,2)) AS ERA
    , IF(@InnPitch=0,0,@FIP := round(((13*i.hra)+(3*(i.bb+i.hp))-(2*i.k))/@InnPitch+f.FIPConstant,2)) AS FIP
    , IF(@InnPitch=0,0,round(((13*(i.fb*f.hr_fb_pct))+(3*(i.bb+i.hp))-(2*i.k))/@InnPitch+f.FIPConstant,2)) AS xFIP
    , round(100*((@ERA + (@ERA - @ERA*(p.avg)))/slg.slgERA),0) AS ERAminus
    , IF(@ERA=0,0,round(100*(slg.slgERA/@ERA)*p.avg,0)) AS ERAplus
    , round(100*((@FIP + (@FIP - @FIP*(p.avg)))/slg.slgFIP),0) AS FIPminus
    FROM players_career_pitching_stats AS i
    INNER JOIN FIPConstant AS f ON i.year=f.year AND i.league_id=f.league_id
    INNER JOIN sub_league_history_pitching AS slg ON i.year=slg.year AND i.league_id=slg.league_id AND i.sub_league_id=slg.sub_league_id
    INNER JOIN teams AS t ON i.team_id=t.team_id
    INNER JOIN parks AS p ON t.park_id=p.park_id
WHERE i.split_id=1 AND i.league_id<>0 AND i.team_id<>0"""

CalcPitching_L= """CREATE TABLE IF NOT EXISTS CalcPitching_L (pit_id INT AUTO_INCREMENT PRIMARY KEY)

SELECT
    i.player_id
    , i.year
    , i.stint
    , i.team_id
    , i.level_id
    , i.league_id
    , i.sub_league_id
    , i.split_id
    , i.ip
    , i.ab
    , i.tb
    , i.ha
    , i.k
    , i.bf
    , i.rs
    , i.bb
    , i.r
    , i.er
    , i.gb
    , i.fb
    , i.pi
    , i.ipf
    , i.g
    , i.gs
    , i.w
    , i.l
    , i.s
    , i.sa
    , i.da
    , i.sh
    , i.sf
    , i.ta
    , i.hra
    , i.bk
    , i.ci
    , i.iw
    , i.wp
    , i.hp
    , i.gf
    , i.dp
    , i.qs
    , i.svo
    , i.bs
    , i.ra
    , i.cg
    , i.sho
    , i.sb
    , i.cs
    , i.hld
    , i.ir
    , i.irs
    , i.wpa
    , i.li
    , i.outs
    , i.war
    , @InnPitch := ((3*ip)+ipf)/3 AS InnPitch
    , IF(@InnPitch=0,0,round((9*i.k)/@InnPitch,1)) AS 'k9'
    , IF(@InnPitch=0,0, round((9*i.bb)/@InnPitch,1)) AS 'bb9'
    , IF(@InnPitch=0,0,round((9*i.hra)/@InnPitch,1)) AS 'HR9'
    , IF(@InnPitch=0,0, round((i.bb+i.ha)/@InnPitch,2)) AS WHIP
    , IF(i.bb=0,0,round(i.k/i.bb,2)) AS 'K/BB'
    , IF(i.fb=0,0,i.gb/i.fb) AS 'gb/fb'
    , IF(i.ab-i.k-i.hra-i.sh+i.sf=0,0,round((i.ha-i.hra)/(i.ab-i.k-i.hra-i.sh+i.sf),3)) AS BABIP
    , IF(@InnPitch=0,0,@ERA := round((i.er/@InnPitch)*9,2)) AS ERA
    , IF(@InnPitch=0,0,@FIP := round(((13*i.hra)+(3*(i.bb+i.hp))-(2*i.k))/@InnPitch+f.FIPConstant,2)) AS FIP
    , IF(@InnPitch=0,0,round(((13*(i.fb*f.hr_fb_pct))+(3*(i.bb+i.hp))-(2*i.k))/@InnPitch+f.FIPConstant,2)) AS xFIP
    , round(100*((@ERA + (@ERA - @ERA*(p.avg)))/slg.slgERA),0) AS ERAminus
    , IF(@ERA=0,0,round(100*(slg.slgERA/@ERA)*p.avg,0)) AS ERAplus
    , round(100*((@FIP + (@FIP - @FIP*(p.avg)))/slg.slgFIP),0) AS FIPminus
    FROM players_career_pitching_stats AS i
    INNER JOIN FIPConstant AS f ON i.year=f.year AND i.league_id=f.league_id
    INNER JOIN sub_league_history_pitching AS slg ON i.year=slg.year AND i.league_id=slg.league_id AND i.sub_league_id=slg.sub_league_id
    INNER JOIN teams AS t ON i.team_id=t.team_id
    INNER JOIN parks AS p ON t.park_id=p.park_id
WHERE i.split_id=2 AND i.league_id<>0 AND i.team_id<>0"""

CalcPitching_R = """CREATE TABLE IF NOT EXISTS CalcPitching_R (pit_id INT AUTO_INCREMENT PRIMARY KEY)
SELECT
    i.player_id
    , i.year
    , i.stint
    , i.team_id
    , i.level_id
    , i.league_id
    , i.sub_league_id
    , i.split_id
    , i.ip
    , i.ab
    , i.tb
    , i.ha
    , i.k
    , i.bf
    , i.rs
    , i.bb
    , i.r
    , i.er
    , i.gb
    , i.fb
    , i.pi
    , i.ipf
    , i.g
    , i.gs
    , i.w
    , i.l
    , i.s
    , i.sa
    , i.da
    , i.sh
    , i.sf
    , i.ta
    , i.hra
    , i.bk
    , i.ci
    , i.iw
    , i.wp
    , i.hp
    , i.gf
    , i.dp
    , i.qs
    , i.svo
    , i.bs
    , i.ra
    , i.cg
    , i.sho
    , i.sb
    , i.cs
    , i.hld
    , i.ir
    , i.irs
    , i.wpa
    , i.li
    , i.outs
    , i.war
    , @InnPitch := ((3*ip)+ipf)/3 AS InnPitch
    , IF(@InnPitch=0,0,round((9*i.k)/@InnPitch,1)) AS 'k9'
    , IF(@InnPitch=0,0, round((9*i.bb)/@InnPitch,1)) AS 'bb9'
    , IF(@InnPitch=0,0,round((9*i.hra)/@InnPitch,1)) AS 'HR9'
    , IF(@InnPitch=0,0, round((i.bb+i.ha)/@InnPitch,2)) AS WHIP
    , IF(i.bb=0,0,round(i.k/i.bb,2)) AS 'K/BB'
    , IF(i.fb=0,0,i.gb/i.fb) AS 'gb/fb'
    , IF(i.ab-i.k-i.hra-i.sh+i.sf=0,0,round((i.ha-i.hra)/(i.ab-i.k-i.hra-i.sh+i.sf),3)) AS BABIP
    , IF(@InnPitch=0,0,@ERA := round((i.er/@InnPitch)*9,2)) AS ERA
    , IF(@InnPitch=0,0,@FIP := round(((13*i.hra)+(3*(i.bb+i.hp))-(2*i.k))/@InnPitch+f.FIPConstant,2)) AS FIP
    , IF(@InnPitch=0,0,round(((13*(i.fb*f.hr_fb_pct))+(3*(i.bb+i.hp))-(2*i.k))/@InnPitch+f.FIPConstant,2)) AS xFIP
    , round(100*((@ERA + (@ERA - @ERA*(p.avg)))/slg.slgERA),0) AS ERAminus
    , IF(@ERA=0,0,round(100*(slg.slgERA/@ERA)*p.avg,0)) AS ERAplus
    , round(100*((@FIP + (@FIP - @FIP*(p.avg)))/slg.slgFIP),0) AS FIPminus
    FROM players_career_pitching_stats AS i
    INNER JOIN FIPConstant AS f ON i.year=f.year AND i.league_id=f.league_id
    INNER JOIN sub_league_history_pitching AS slg ON i.year=slg.year AND i.league_id=slg.league_id AND i.sub_league_id=slg.sub_league_id
    INNER JOIN teams AS t ON i.team_id=t.team_id
    INNER JOIN parks AS p ON t.park_id=p.park_id
WHERE i.split_id=3 AND i.league_id<>0 AND i.team_id<>0"""