import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# ── CHANGE 1: Add tab9 to the tab declaration ──
old_tabs = '''    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(
        ["📊 Overview", "⚠️ Churn", "💰 Revenue & Inflation (CAGR)", "🔮 Predictive Trends", "🏥 Clinical Insights", "🔍 Data Quality", "🏥 Branch Ops", "💎 Revenue Mix"])'''

new_tabs = '''    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs(
        ["📊 Overview", "⚠️ Churn", "💰 Revenue & Inflation (CAGR)", "🔮 Predictive Trends", "🏥 Clinical Insights", "🔍 Data Quality", "🏥 Branch Ops", "💎 Revenue Mix", "⚔️ Branch Compare"])'''

if old_tabs in content:
    content = content.replace(old_tabs, new_tabs, 1)
    print("CHANGE 1 APPLIED: Added tab9 (Branch Compare)")
else:
    print("CHANGE 1 ERROR: Could not find tab declaration")

# ── CHANGE 2: Add CAGR charts after the inflation note ──
old_cagr_end = '''            st.info(f"📌 **Inflation Note:** Real CAGR = **{cagr_real:+.1f}%** after Egypt's ~{INFL*100:.0f}%/yr inflation")

    # ── TAB 4: PREDICTIVE TRENDS ──'''

new_cagr_end = '''            st.info(f"📌 **Inflation Note:** Real CAGR = **{cagr_real:+.1f}%** after Egypt's ~{INFL*100:.0f}%/yr inflation")

            # ── Chart 1: Nominal vs Real Revenue ──
            sec_title("📈 Nominal vs Real Revenue Over Time",
                      "Blue = actual EGP received | Green = inflation-adjusted purchasing power")
            chart_start()
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=mr["visit_month"], y=mr["total_revenue"],
                mode="lines+markers", name="Nominal Revenue",
                line=dict(color="#1a73e8", width=3), marker=dict(size=8)
            ))
            fig.add_trace(go.Scatter(
                x=mr["visit_month"], y=mr["real_revenue"],
                mode="lines+markers", name="Real Revenue",
                line=dict(color="#34a853", width=3), marker=dict(size=8)
            ))
            # Fill the gap between nominal and real
            fig.add_trace(go.Scatter(
                x=list(mr["visit_month"]) + list(mr["visit_month"][::-1]),
                y=list(mr["total_revenue"]) + list(mr["real_revenue"][::-1]),
                fill="toself", fillcolor="rgba(234,67,53,0.15)",
                line=dict(color="rgba(0,0,0,0)"), hoverinfo="skip",
                name="Inflation Erosion", showlegend=True
            ))
            google_theme(fig, height=350)
            fig.update_layout(
                xaxis=dict(tickformat="%b %Y", dtick="M1"),
                yaxis_title="Revenue (EGP)",
                hovermode="x unified",
                legend=dict(orientation="h", yanchor="bottom", y=1.02)
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            chart_end()

            # ── Chart 2: Revenue Index Comparison ──
            sec_title("📊 Revenue Index — Nominal vs Real (Base = 100)",
                      "Shows how purchasing power erodes even when nominal numbers rise")
            chart_start()
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=mr["visit_month"], y=mr["nominal_index"],
                mode="lines+markers", name="Nominal Index",
                line=dict(color="#1a73e8", width=3), marker=dict(size=8)
            ))
            fig.add_trace(go.Scatter(
                x=mr["visit_month"], y=mr["real_index"],
                mode="lines+markers", name="Real Index",
                line=dict(color="#34a853", width=3), marker=dict(size=8)
            ))
            fig.add_hline(y=100, line_dash="dash", line_color="#9aa0a6",
                         annotation_text="Base = 100", annotation_position="top right")
            google_theme(fig, height=320)
            fig.update_layout(
                xaxis=dict(tickformat="%b %Y", dtick="M1"),
                yaxis_title="Index (Base = 100)",
                hovermode="x unified",
                legend=dict(orientation="h", yanchor="bottom", y=1.02)
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            chart_end()

            # ── Chart 3: Monthly Inflation Tax ──
            sec_title("🔥 Monthly Inflation Erosion",
                      "How much revenue purchasing power is lost each month")
            chart_start()
            fig = px.bar(mr, x="visit_month", y="inflation_tax",
                        color="inflation_tax", color_continuous_scale="Reds",
                        text=mr["inflation_tax"].apply(lambda x: f"{x/1000:.0f}K"))
            fig.update_traces(textposition="outside")
            google_theme(fig, height=300)
            fig.update_layout(
                xaxis=dict(tickformat="%b %Y", dtick="M1"),
                yaxis_title="EGP Lost to Inflation",
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            chart_end()

    # ── TAB 4: PREDICTIVE TRENDS ──'''

if old_cagr_end in content:
    content = content.replace(old_cagr_end, new_cagr_end, 1)
    print("CHANGE 2 APPLIED: Added 3 CAGR charts")
else:
    print("CHANGE 2 ERROR: Could not find CAGR section end")

# ── CHANGE 3: Add Branch vs Branch comparison tab before PAGE: EXPORT ──
old_export_section = '''# ============================================================
# PAGE: EXPORT
# ============================================================

elif page == "📥  Export":'''

new_tab9 = '''    # ── TAB 9: BRANCH VS BRANCH COMPARISON ──
    with tab9:
        sec_title("⚔️ Branch vs Branch Comparison", "Head-to-head performance analysis")
        if "Branch_Name" in filtered_visits.columns:
            branches_list = sorted(filtered_visits["Branch_Name"].unique().tolist())
            if len(branches_list) >= 2:
                c1, c2 = st.columns(2)
                with c1:
                    branch_a = st.selectbox("🏥 Branch A", branches_list, index=0, key="branch_a")
                with c2:
                    branch_b = st.selectbox("🏥 Branch B", branches_list, index=min(1, len(branches_list)-1), key="branch_b")

                # Compute metrics dynamically based on available columns
                agg_dict = {}
                if "Visit_ID" in filtered_visits.columns:
                    agg_dict["total_visits"] = ("Visit_ID", "count")
                if "Patient_ID" in filtered_visits.columns:
                    agg_dict["unique_patients"] = ("Patient_ID", "nunique")
                if "Amount_Paid" in filtered_visits.columns:
                    agg_dict["revenue"] = ("Amount_Paid", "sum")
                if "Visit_Duration" in filtered_visits.columns:
                    agg_dict["avg_duration"] = ("Visit_Duration", "mean")

                if agg_dict:
                    bm = filtered_visits.groupby("Branch_Name").agg(**agg_dict).reset_index()
                    if "revenue" in bm.columns and "total_visits" in bm.columns:
                        bm["revenue_per_visit"] = (bm["revenue"] / bm["total_visits"]).round(0)

                    a_row = bm[bm["Branch_Name"] == branch_a]
                    b_row = bm[bm["Branch_Name"] == branch_b]
                    a_data = a_row.iloc[0] if not a_row.empty else None
                    b_data = b_row.iloc[0] if not b_row.empty else None

                    if a_data is not None and b_data is not None:
                        # Comparison KPI row
                        def diff_card(label, col, icon, accent_a, accent_b):
                            a_val = int(a_data[col]) if col in a_data.index else 0
                            b_val = int(b_data[col]) if col in b_data.index else 0
                            diff = a_val - b_val
                            if diff > 0:
                                return kpi_card(f"{label} (A)", f"{a_val:,}", f"+{diff:,} vs B", "up", icon, accent_a)
                            elif diff < 0:
                                return kpi_card(f"{label} (A)", f"{a_val:,}", f"{diff:,} vs B", "down", icon, accent_a)
                            else:
                                return kpi_card(f"{label} (A)", f"{a_val:,}", "Tied with B", "neutral", icon, "#fbbc04")

                        cards = []
                        if "total_visits" in bm.columns:
                            cards.append(diff_card("Visits", "total_visits", "📊", "#1a73e8", "#ea4335"))
                        if "unique_patients" in bm.columns:
                            cards.append(diff_card("Patients", "unique_patients", "👥", "#34a853", "#ea4335"))
                        if "revenue" in bm.columns:
                            a_rev = int(a_data["revenue"]) if "revenue" in a_data.index else 0
                            b_rev = int(b_data["revenue"]) if "revenue" in b_data.index else 0
                            diff_rev = a_rev - b_rev
                            trend = "up" if diff_rev > 0 else "down" if diff_rev < 0 else "neutral"
                            cards.append(kpi_card("Revenue A", f"{a_rev/1000:.1f}K", f"{diff_rev/1000:+.1f}K vs B", trend, "💰", "#9334e6"))
                        if "revenue_per_visit" in bm.columns:
                            a_rpv = int(a_data["revenue_per_visit"]) if "revenue_per_visit" in a_data.index else 0
                            b_rpv = int(b_data["revenue_per_visit"]) if "revenue_per_visit" in b_data.index else 0
                            diff_rpv = a_rpv - b_rpv
                            trend = "up" if diff_rpv > 0 else "down" if diff_rpv < 0 else "neutral"
                            cards.append(kpi_card("Rev/Visit A", f"{a_rpv:,}", f"{diff_rpv:+,} vs B", trend, "💵", "#fbbc04"))
                        if "avg_duration" in bm.columns:
                            a_dur = int(a_data["avg_duration"]) if "avg_duration" in a_data.index else 0
                            b_dur = int(b_data["avg_duration"]) if "avg_duration" in b_data.index else 0
                            diff_dur = a_dur - b_dur
                            trend = "up" if diff_dur > 0 else "down" if diff_dur < 0 else "neutral"
                            cards.append(kpi_card("Duration A", f"{a_dur} min", f"{diff_dur:+,} vs B", trend, "⏱️", "#1a73e8"))

                        if cards:
                            st.markdown(kpi_row(cards, cols=len(cards)), unsafe_allow_html=True)

                        # Grouped bar chart comparison
                        sec_title("📊 Side-by-Side Comparison", "Key metrics across selected branches")
                        chart_start()
                        compare_cols = [c for c in ["total_visits", "unique_patients", "revenue", "revenue_per_visit"] if c in bm.columns]
                        if compare_cols:
                            compare_df = bm[bm["Branch_Name"].isin([branch_a, branch_b])].copy()
                            # Melt for grouped bar chart
                            melted = compare_df.melt(id_vars=["Branch_Name"], value_vars=compare_cols,
                                                     var_name="Metric", value_name="Value")
                            metric_labels = {
                                "total_visits": "Total Visits",
                                "unique_patients": "Unique Patients",
                                "revenue": "Revenue",
                                "revenue_per_visit": "Rev/Visit"
                            }
                            melted["Metric"] = melted["Metric"].map(metric_labels)
                            fig = px.bar(melted, x="Metric", y="Value", color="Branch_Name",
                                         barmode="group", color_discrete_map={branch_a: "#1a73e8", branch_b: "#34a853"},
                                         text="Value")
                            fig.update_traces(textposition="outside")
                            google_theme(fig, height=350)
                            fig.update_layout(xaxis_title=None, yaxis_title="Value",
                                              legend=dict(orientation="h", yanchor="bottom", y=1.02))
                            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
                        chart_end()

                        # Difference table
                        info_card_start("📋 Metric Comparison Table")
                        diff_data = []
                        for col in compare_cols:
                            a_v = a_data[col] if col in a_data.index else 0
                            b_v = b_data[col] if col in b_data.index else 0
                            label = metric_labels.get(col, col)
                            diff_data.append({
                                "Metric": label,
                                f"{branch_a}": f"{a_v:,.0f}",
                                f"{branch_b}": f"{b_v:,.0f}",
                                "Difference": f"{a_v - b_v:+,}",
                                "Winner": "A" if a_v > b_v else "B" if b_v > a_v else "Tie"
                            })
                        diff_df = pd.DataFrame(diff_data)
                        st.dataframe(diff_df, hide_index=True, use_container_width=True)
                        info_card_end()
                    else:
                        st.warning("Could not retrieve data for one or both branches")
                else:
                    st.info("No aggregatable columns available for comparison")
            else:
                st.info("Need at least 2 branches to compare")
        else:
            st.info("Branch_Name column not available in visits data")

# ============================================================
# PAGE: EXPORT
# ============================================================

elif page == "📥  Export":'''

if old_export_section in content:
    content = content.replace(old_export_section, new_tab9, 1)
    print("CHANGE 3 APPLIED: Added Branch vs Branch comparison tab")
else:
    print("CHANGE 3 ERROR: Could not find PAGE: EXPORT section")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("All changes written to app.py")
