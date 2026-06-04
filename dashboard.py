# =====================
    # AUTONOMOUS EXECUTION
    # =====================

    st.subheader("⚡ Agent Execution Center")


    if direction == "LONG 📈":

        action = "OPEN LONG POSITION 📈"
        execution = "Virtual Trade Created ✅"


    elif direction == "SHORT 📉":

        action = "OPEN SHORT POSITION 📉"
        execution = "Virtual Trade Created ✅"


    else:

        action = "NO POSITION ⏳"
        execution = "Waiting For Opportunity"


    e1,e2 = st.columns(2)


    e1.metric(
        "🤖 Agent Action",
        action
    )


    e2.metric(
        "⚙️ Execution",
        execution
    )


    st.subheader("🧾 Agent Memory")


    memory = {
        "Asset": symbol,
        "Decision": direction,
        "Confidence": confidence,
        "SL": sl,
        "TP": tp
    }


    st.json(memory)
